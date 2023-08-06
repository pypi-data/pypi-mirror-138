import click
from gopublic.cli.commands.file.delete import cli as delete
from gopublic.cli.commands.file.list import cli as list
from gopublic.cli.commands.file.publish import cli as publish
from gopublic.cli.commands.file.search import cli as search
from gopublic.cli.commands.file.tag import cli as tag
from gopublic.cli.commands.file.unpublish import cli as unpublish
from gopublic.cli.commands.file.untag import cli as untag


@click.group()
def cli():
    """
    Manipulate files managed by Gopublish
    """
    pass


cli.add_command(delete)
cli.add_command(list)
cli.add_command(publish)
cli.add_command(search)
cli.add_command(tag)
cli.add_command(unpublish)
cli.add_command(untag)
