from typing import Any, List

from automcp.models import (
    TasksTag,
    ModelBooleanResponse
)

from automcp.llm.task import LLMTask
from automcp.logger import setup_logging


logger = setup_logging(__name__)


SYS_PROMPT = """Given below is a man page description of a command.
You must return true if the man page has sub-commands, otherwise false.
- Do NOT under any circumstances try to generate a code. Keep your response short.
- Do NOT consider arguments, flags, options as sub-commands.
- If there is explicit mention of title "commands" or "subcommands" or similar then return true, otherwise false.
"""

USER_PROMPT = """### Query
{query}
"""

class DetectSubCommands(LLMTask):
    """
    Detects sub-commands from the user query.
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
        return [TasksTag.detect_sub_commands] + self._tags

    def preprocess(self):
        return {
            "query": self.query
        }

    def prompt(self):
        return {"system": SYS_PROMPT, "user": USER_PROMPT}

    def postprocess(self, result: str) -> ModelBooleanResponse:
        tags = self.tags
        check_result = result.lower().lstrip().startswith("true")
        return ModelBooleanResponse(
            bool_value=check_result,
            text=result,
            tags=tags,
            metadata=self.metadata
        )
