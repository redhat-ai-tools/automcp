from enum import Enum
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

COMMAND_HELP = "{program} {help_command}"

DUMMY_PROMPT_TOKEN = "|%|"
DUMMY_PROMPT = "{system}|%|{user}"

# LLM Tasks
class TasksTag(str, Enum):
    detect_sub_commands = "detect_sub_commands"
    extract_command = "extract_command"
    extract_command_list = "extract_command_list"


# LLM Response
class ModelResponse(BaseModel):
    tags: list = []
    text: str = ""
    metadata: Any = None


class ModelResponseList(ModelResponse):
    items: List[str | Dict | Any] = []


class ModelResponseDict(ModelResponse):
    data: Dict[str, Any] = {}


class ModelBooleanResponse(ModelResponse):
    bool_value: bool


class ModelResponseData(ModelResponse):
    data: Any


# Models for command extraction

class Argument(BaseModel):
    name: str
    optional: bool

class Option(BaseModel):
    flag: str
    description: str
    short_option: Optional[str]
    type: str

class Command(BaseModel):
    description: str
    arguments: List[Argument]
    options: List[Option]

class CommandItem(BaseModel):
    command: str
    data: Command
