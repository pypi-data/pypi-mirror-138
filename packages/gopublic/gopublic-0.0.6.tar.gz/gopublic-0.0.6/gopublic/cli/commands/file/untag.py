import click
from gopublic.cli.cli import pass_context, json_loads
from gopublic.cli.decorators import custom_exception, dict_output


@click.command('untag')
@click.argument("file_id", type=str)
@click.option(
    "--tags",
    help="Comma-separated tags to add",
    type=str
)
@click.option(
    "--token",
    help="Your Gopublish token.",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_id, tags="", token=""):
    """Remove one or more tag from a file

Output:

    Dict with file state
    """
    return ctx.gi.file.untag(file_id, tags=tags, token=token)
