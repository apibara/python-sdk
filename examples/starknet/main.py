import sys
import asyncio
from argparse import ArgumentParser
from datetime import datetime

from apibara import NewEvents, IndexerRunner, NewBlock, Info, Client
from apibara.model import EventFilter


INDEXER_ID = 'starknet-example'
BRIQS_ADDRESS = '0x0266b1276d23ffb53d99da3f01be7e29fa024dd33cd7f7b1eb7a46c67891c9d0'


async def handle_events(_info: Info, block_events: NewEvents):
    print('block ', block_events.block_number)
    for event in block_events.events:
        print('   ', event)


async def handle_block(info: Info, block: NewBlock):
    # Use the provided RPC client to fetch the current block data.
    # The client is already initialized with the correct network based
    # on the indexer's settings.
    block = await info.rpc_client.get_block_by_hash(block.new_head.hash)
    block_time = datetime.fromtimestamp(block['accepted_time'])
    print('new live block', block_time)


async def main(args):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true", default=False)
    args = parser.parse_args()

    if args.reset:
        async with Client.connect() as client:
            await client.indexer_client().delete_indexer(INDEXER_ID)
            print('Indexer deleted. Starting from beginning.')

    runner = IndexerRunner(
        indexer_id=INDEXER_ID,
        new_events_handler=handle_events,
    )

    runner.add_block_handler(handle_block)

    # Create the indexer if it doesn't exist on the server,
    # otherwise it will resume indexing from where it left off.
    #
    # For now, this also helps the SDK map between human-readable
    # event names and StarkNet events.
    runner.create_if_not_exists(
        filters=[
            EventFilter.from_event_name(
                name='Transfer',
                address=BRIQS_ADDRESS
            )
        ], 
        index_from_block=201_000
    )

    await runner.run()


if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
