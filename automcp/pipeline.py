from automcp.llm.executor import LLMTaskExecutor
from typing import cast
from automcp.llm.tasks.extract_command import Command, ExtractCommand
from automcp.models import (
    COMMAND_HELP,
    CommandItem,
    ModelBooleanResponse,
    ModelResponseData,
)
from automcp.logger import setup_logging
from automcp.utils import run_shell
from automcp.llm.tasks.detect_sub_commands import DetectSubCommands
from automcp.templates.generator import create_server_template

logger = setup_logging(__name__)


class AutoMCP_Pipeline:
    def __init__(self):
        self.executor = LLMTaskExecutor()

    def run(self, program: str, help_command: str):
        '''Run the pipeline for a given program to generate MCP server.'''
        sub_commands = self._detect_sub_commands(program, help_command)
        logger.debug("No. of sub-commands: %d", len(sub_commands))

        server_template = create_server_template(sub_commands)
        logger.debug("Server template: %s", server_template)


    def _detect_sub_commands(self, program: str, help_command: str):
        '''Recursively detect sub-commands from the help docs.'''
        help_docs = run_shell(
            COMMAND_HELP.format(program=program, help_command=help_command)
        )
        logger.debug("Length of help docs: %d", len(help_docs))
        # logger.debug("First 100 chars of help docs: %s", help_docs[:100] + "...")

        if self.check_sub_command_exists(help_docs):
            return []
            # return self._detect_sub_commands(program, help_command)
        else:
            return [self.extract_command(program, help_docs)]

    def check_sub_command_exists(self, help_docs: str):
        '''Check if the help docs contain sub-commands.'''
        result = self.executor.run(
            DetectSubCommands(query=help_docs)
        )
        result = cast(ModelBooleanResponse, result)
        return result.bool_value

    def extract_command(self, command: str, help_docs: str) -> CommandItem:
        '''Extract the command from the help docs.'''
        result = self.executor.run(
            ExtractCommand(query=help_docs)
        )
        result = cast(ModelResponseData, result)
        data = cast(Command, result.data)
        return CommandItem(command=command, data=data)
