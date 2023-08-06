"""Main module."""
import click

from .add_todoist_task import add_todoist_task


@click.group()
def cli():
    """
    Main group.
    """


@click.command()
@click.option('-p', '--project_id')
def add(project_id):
    """
    Add a new todoist task to the inbox.
    """
    add_todoist_task(project_id)
    click.echo("Logged.")


cli.add_command(add)
