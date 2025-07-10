import click
import os
from automcp import VERSION
from automcp.pipeline import AutoMCP_Pipeline

@click.group()
@click.version_option(VERSION, "-v", "--version")
def cli():
    pass

@cli.command()
@click.option("--program", "-p", help="Path to script, CLI, or executable", required=True)
@click.option("--help_command", "-hc", help="Name of the help command", default="--help")
@click.option("--output", "-o", help="Save path for the MCP server", default="./server.py")
def create(program, help_command, output):
    click.echo(f"Creating MCP server for project: {program}")

    pipeline = AutoMCP_Pipeline()
    server_template = pipeline.run(program, help_command)

    head, _ = os.path.split(output)
    os.makedirs(head, exist_ok=True)
    with open(output, "w") as f:
        f.write(server_template)
    click.echo(f"MCP server tool created at {output}") 

if __name__ == "__main__":
    cli()
