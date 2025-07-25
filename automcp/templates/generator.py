import jinja2
import os
import re
from typing import List
from automcp.models import Argument, CommandItem, Option

environment = jinja2.Environment()
# Add enumerate to the template environment so it's available in templates
environment.globals['enumerate'] = enumerate

def process_safe_name(command: str):
    command = command.strip()\
        .lower()\
        .replace("-", "_")\
        .replace(" ", "_")\
        .replace(":", "_")\
        .replace(".", "")\
        .replace("*", "")\
        .replace("|", "")

    # Remove all non-alphanumeric characters except underscore
    command = re.sub(r'[^a-zA-Z0-9_]', '', command)

    return command

def process_flag_name(flag: str):
    '''
    Convert a flag name to a safe name.
    e.g. --help -> help
    e.g. --help-long -> help_long
    '''
    flag = flag.strip()
    if flag.startswith("--"):
        flag = flag[2:]
    flag = flag.replace("-", "_")
    return flag

def prepare_arg(arg: Argument):
    return {
        "name": process_safe_name(arg.name),
    }

def preprocess_args(args: List[Argument]):
    # Case when multiple arguments have same name.
    # e.g. kubectl get pods
    arg_names = [process_safe_name(x.name) for x in args]
    if len(set(arg_names)) == 1 and len(arg_names) > 1:
        return [
            Argument(
                name=f"*{process_safe_name(args[0].name)}",
                optional=False,
            )
        ]
    return [prepare_arg(arg) for arg in args]

def preprocess_flags(flags: List[Option]):
    return [
        {
            "flag": flag.flag,
            "flag_name": process_flag_name(flag.flag),
            "description": flag.description,
            "type": flag.type
        }
        for flag in flags
    ]

def prepare_command(command: CommandItem):
    args = preprocess_args(command.data.arguments)
    flags = preprocess_flags(command.data.options)
    return {
        "command": command.command,
        "description": command.data.description,
        "function": process_safe_name(command.command),
        "args": args,
        "flags": flags
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
