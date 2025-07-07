import click
from automcp import VERSION

@click.group()
@click.version_option(VERSION, "-v", "--version")
def cli():
    pass

if __name__ == "__main__":
    cli()
