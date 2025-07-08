import click
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
    pipeline.run(program, help_command)


if __name__ == "__main__":
    cli()
