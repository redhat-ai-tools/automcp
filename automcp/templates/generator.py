import jinja2
import os
from typing import List
from automcp.models import Argument, CommandItem

environment = jinja2.Environment()
# Add enumerate to the template environment so it's available in templates
environment.globals['enumerate'] = enumerate

def process_safe_name(command: str):
    return command.strip().replace("-", "_").replace(" ", "_").replace(":", "_").lower()

def prepare_arg(arg: Argument):
    return {
        "name": process_safe_name(arg.name),
    }

def combine_args(args: List[Argument]):
    if len(set([x.name for x in args])) == 1:
        return [
            Argument(
                name=f"*{args[0].name}",
                optional=False,
            )
        ]

    return args

def prepare_command(command: CommandItem):
    args = combine_args(command.data.arguments)

    return {
        "command": command.command,
        "description": command.data.description,
        "function": process_safe_name(command.command),
        "args": [ prepare_arg(arg) for arg in args ],
    }


def create_server_template(commands: List[CommandItem]) -> str:
    # Get the directory of the current module
    current_dir = os.path.dirname(__file__)
    template_path = os.path.join(current_dir, "server.j2")
    
    template_str = open(template_path).read()
    template = environment.from_string(template_str)
    return template.render(
        name=(commands[0].command.split()[0] if len(commands) > 0 else "AutoMCP"),
        commands=list(map(prepare_command, commands))
    )
