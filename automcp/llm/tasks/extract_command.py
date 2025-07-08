from typing import Any, List, Optional
from pydantic import BaseModel

from automcp.models import (
    ModelResponse,
    TasksTag,
    ModelResponseData
)

from automcp.llm.task import LLMTask
from automcp.logger import setup_logging


logger = setup_logging(__name__)


SYS_PROMPT = """You are a documentation extractor. 
Given the raw man-page text for a command, parse it into JSON using the following rules:
- Arguments
    - Include only positional arguments.
    - name is exactly as shown (e.g. file, pattern).
    - optional is true if the synopsis encloses it in brackets ([ ]), else false.
- Options
    - name: the full flag (always starts with --).
    - short_name: the single-hyphen alias (starts with -), or "" if none.
    - type: data type (e.g. integer, string) if the option takes argument and type is mentioned, else "".
- Do not invent flags or arguments—only extract what's present.
"""

USER_PROMPT = """### Query
{query}
"""

class Argument(BaseModel):
    name: str
    optional: bool

class Option(BaseModel):
    name: str
    description: str
    short_name: Optional[str] = ""
    type: str

class Command(BaseModel):
    name: str
    description: str
    arguments: List[Argument]
    options: List[Option]

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

    def preprocess(self):
        return {
            "query": self.query
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
