import click
from gopublic.cli.cli import pass_context, json_loads
from gopublic.cli.decorators import custom_exception, dict_output


@click.command('search')
@click.option(
    "--query",
    help="Either a search term, or a file UID",
    type=str
)
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
def cli(ctx, query="", tags="", limit="", offset=""):
    """Launch a pull task

Output:

    Dict with files and total count
    """
    return ctx.gi.file.search(query=query, tags=tags, limit=limit, offset=offset)
