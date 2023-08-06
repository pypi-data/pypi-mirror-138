import click
from gopublic.cli.cli import pass_context, json_loads
from gopublic.cli.decorators import custom_exception, dict_output


@click.command('publish')
@click.argument("path", type=str)
@click.option(
    "--tags",
    help="Comma-separated tags",
    type=str
)
@click.option(
    "--linked_to",
    help="id of the original file this file is a version of",
    type=str
)
@click.option(
    "--contact",
    help="Contact email for this file",
    type=str
)
@click.option(
    "--email",
    help="Contact email for notification when publication is done",
    type=str
)
@click.option(
    "--token",
    help="Your Gopublish token.",
    type=str
)
@click.option(
    "--inherit_tags",
    help="Inherit linked file tags. Default to True",
    default="True",
    show_default=True,
    is_flag=True
)
@pass_context
@custom_exception
@dict_output
def cli(ctx, path, tags="", linked_to="", contact="", email="", token="", inherit_tags=True):
    """Launch a publish task

Output:

    Dictionnary containing the response
    """
    return ctx.gi.file.publish(path, tags=tags, linked_to=linked_to, contact=contact, email=email, token=token, inherit_tags=inherit_tags)
