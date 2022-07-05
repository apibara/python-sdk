import asyncio
from audioop import add
from typing import Iterator

from apibara import NewEvents, IndexerRunner, NewBlock
from apibara.model import EventFilter


INDEXER_ID = 'starknet-example'
BRIQS_ADDRESS = '0x0266b1276d23ffb53d99da3f01be7e29fa024dd33cd7f7b1eb7a46c67891c9d0'


async def handle_events(_info, block_events: NewEvents):
    print('block ', block_events.block_number)
    for event in block_events.events:
        print('   ', event)


async def handle_block(_info, block: NewBlock):
    print('new live block', block.new_head.number)


async def main():
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
    asyncio.run(main())
