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
@click.option("--output", "-o", help="Path to output directory", default=".")
def create(program, help_command, output):
    click.echo(f"Creating MCP server for project: {program}")

    pipeline = AutoMCP_Pipeline()
    server_template = pipeline.run(program, help_command)

    os.makedirs(output, exist_ok=True)
    filename = f"{program.lower().replace(' ', '-').replace('-', '-')}-server.py"
    filepath = os.path.join(output, filename)
    with open(filepath, "w") as f:
        f.write(server_template)

    click.echo(f"MCP server tool created at {filepath}") 

if __name__ == "__main__":
    cli()
