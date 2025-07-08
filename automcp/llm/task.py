from abc import ABC, abstractmethod
from typing import Any

from automcp.models import ModelResponse


class LLMTask(ABC):

    @property
    @abstractmethod
    def tags(self):
        pass

    @abstractmethod
    def preprocess(self, *args, **kwargs) -> dict:
        # Takes in data input and returns a key:valued pair items of inputs passed to prompt()
        pass

    @abstractmethod
    def prompt(self, **kwargs) -> dict[str, str]:
        # Takes key:valued argumets from preprocess results and returns the query prompt for LLM
        pass

    @abstractmethod
    def postprocess(self, response: str | Any) -> ModelResponse:
        # Takes in raw string response from LLM and returns a ModelResponse object
        pass
