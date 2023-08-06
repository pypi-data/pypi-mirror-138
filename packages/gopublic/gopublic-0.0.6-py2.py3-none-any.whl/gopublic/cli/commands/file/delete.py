import click
from gopublic.cli.cli import pass_context, json_loads
from gopublic.cli.decorators import custom_exception, dict_output


@click.command('delete')
@click.argument("file_id", type=str)
@click.option(
    "--token",
    help="Your Gopublish token.",
    type=str
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, file_id, token=""):
    """Delete a file (admin_restricted)

Output:

    Dictionnary containing the response
    """
    return ctx.gi.file.delete(file_id, token=token)
