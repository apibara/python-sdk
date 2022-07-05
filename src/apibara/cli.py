"""Apibara CLI. Manage applications and indexers from the command line."""

import asyncio
from email.policy import default
from functools import wraps

import click
import grpc
from click_help_colors import HelpColorsGroup

from apibara.client import Client
from apibara.model import EventFilter, Indexer


def async_command(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.group(
    cls=HelpColorsGroup, help_headers_color="cyan", help_options_color="magenta"
)
def cli():
    pass


@cli.group()
def indexer():
    """Manage indexers."""
    pass


@indexer.command()
@click.argument("indexer-id", type=str)
@click.argument("event-name", type=str)
@click.option("--index-from-block", type=int, help="Start indexing from this block.")
@click.option("--address", type=str, help="Only index events emitted by this contract.")
@click.option("--server-url", type=str, default=None, help="Apibara server url.")
@async_command
async def create(
    indexer_id, event_name, index_from_block=None, address=None, server_url=None
):
    """Create a new indexer.

    The indexer is identified by its INDEXER_ID. By default, the indexer indexes all
    events with name EVENT_NAME from block 0.

    The indexer is not started after creation, you need to connect to it to start indexing.
    """
    async with Client.connect(server_url) as client:
        try:
            filter = EventFilter.from_event_name(event_name, address)
            new_indexer = await client.indexer_client().create_indexer(
                indexer_id, index_from_block, filter
            )
            _format_indexer(new_indexer)
        except Exception as ex:
            _format_exception(ex)


@indexer.command()
@click.option("--server-url", type=str, default=None, help="Apibara server url.")
@async_command
async def list(server_url=None):
    """List all available indexers."""
    async with Client.connect(server_url) as client:
        try:
            indexers = await client.indexer_client().list_indexer()
            for indexer in indexers:
                _format_indexer(indexer)
        except Exception as ex:
            _format_exception(ex)


@indexer.command()
@click.argument("indexer-id", type=str)
@click.option("--server-url", type=str, default=None, help="Apibara server url.")
@async_command
async def delete(indexer_id, server_url=None):
    """Delete the given indexer."""
    async with Client.connect(server_url) as client:
        try:
            indexer = await client.indexer_client().delete_indexer(indexer_id)
            _format_indexer(indexer)
        except Exception as ex:
            _format_exception(ex)


def _format_indexer(indexer: Indexer):
    click.secho(indexer.id, fg="cyan")
    blocks = click.style(
        f"[{indexer.index_from_block}, {indexer.indexed_to_block}]", fg="magenta"
    )
    click.echo(f"    blocks: {blocks}")
    click.echo(f"    filters:")
    for filter in indexer.filters:
        if filter.address == b"" or filter.address is None:
            address = "any"
        else:
            address = "0x" + filter.address.hex()
        address = click.style(address, fg="magenta")
        click.echo(f"    - address: {address}")
        click.echo(f"      topics:")
        for topic in filter.topics:
            topic = click.style(topic, fg="magenta")
            click.echo(f"      - {topic}")


def _format_exception(ex: Exception):
    if isinstance(ex, grpc.aio.AioRpcError):
        message = f"({ex.code()}) {ex.details()}"
    else:
        message = str(ex)
    click.secho(message, fg="red")
