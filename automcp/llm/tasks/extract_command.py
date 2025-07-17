import re
from typing import Any, List


from automcp.models import (
    TasksTag,
    ModelResponseData,
    Command,
)

from automcp.llm.task import LLMTask
from automcp.logger import setup_logging


logger = setup_logging(__name__)


SYS_PROMPT = """Given the man page for a command utility, parse it into JSON using the following rules:
- Arguments Rules:
    - include positional arguments.
    - name is exactly as shown (e.g. file, pattern).
    - optional is true if the synopsis encloses it in brackets ([]), else false.
- Options Rules: 
    - flag: complete flag name (e.g. --help, --version).
    - type: if the option takes argument and type is mentioned, else "".
- Only extract what is present.
"""

USER_PROMPT = """### Query
{query}
"""

class ExtractCommand(LLMTask):
    """
    Extracts command from the user query.
    """

    def __init__(
        self,
        query: str,
        tags: List = [],
        metadata: Any = None
    ):
        self._tags = tags
        self.query = query
        self.metadata = metadata

    @property
    def tags(self):
        return [TasksTag.extract_command] + self._tags

    def _preprocess_command_string(self, command: str) -> str:
        command = command.strip()
        # Remove short flags like -h, -v, etc.
        command = re.sub(r'-\w(?!\w)', '', command)
        return command

    def preprocess(self):
        return {
            "query": self._preprocess_command_string(self.query)
        }

    def prompt(self):
        return {
            "system": SYS_PROMPT,
            "user": USER_PROMPT,
            "response_format": Command,
        }

    def postprocess(self, result: Command) -> ModelResponseData:
        tags = self.tags
        return ModelResponseData(
            data=result,
            tags=tags,
            metadata=self.metadata
        )
