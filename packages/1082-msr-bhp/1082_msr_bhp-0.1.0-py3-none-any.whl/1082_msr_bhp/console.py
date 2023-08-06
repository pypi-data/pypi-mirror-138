# src/hypermodern_python/console.py
import os
import click

from . import __version__


@click.command()
@click.version_option(version=__version__)
def main():
    click.echo("Hello, world!")
    click.echo(os.getcwd())