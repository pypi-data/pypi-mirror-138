import click
from gopublic.cli.cli import pass_context, json_loads
from gopublic.cli.decorators import custom_exception, dict_output


@click.command('list')
@click.option(
    "--tags",
    help="Comma-separated tags",
    type=str
)
@click.option(
    "--limit",
    help="Limit the results numbers",
    type=int
)
@click.option(
    "--offset",
    help="Offset for listing the results (used with limit)",
    type=int
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, tags="", limit="", offset=""):
    """List files published in Gopublish

Output:

    Dict with files and total count
    """
    return ctx.gi.file.list(tags=tags, limit=limit, offset=offset)
