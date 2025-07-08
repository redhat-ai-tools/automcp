from typing import Any, List
from pydantic import BaseModel

from automcp.models import (
    ModelResponse,
    TasksTag,
    ModelResponseDict
)

from automcp.llm.task import LLMTask
from automcp.logger import setup_logging


logger = setup_logging(__name__)


SYS_PROMPT = """Given below is a man page description of a command.
You must return JSON object with the following fields:
- description: str
- arguments: list[argument]
- options: list[option]

argument:
- name: str
- optional: bool

option:
- name: str
- description: str
- short_name: str
- type: str

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
    short_name: str
    type: str

class Command(BaseModel):
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

    def postprocess(self, result: dict) -> ModelResponseDict:
        tags = self.tags
        return ModelResponseDict(
            data=result,
            tags=tags,
            metadata=self.metadata
        )
