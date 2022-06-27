import asyncio
from typing import Iterator

from apibara import IndexerManagerClient, DEFAULT_APIBARA_SERVER_URL
from apibara.client import contract_event_filter
from apibara.model import NewEvents


INDEXER_ID = 'starknet-example'
BRIQS_ADDRESS = '0x0266b1276d23ffb53d99da3f01be7e29fa024dd33cd7f7b1eb7a46c67891c9d0'

FILTERS = [
    contract_event_filter('Transfer', address=BRIQS_ADDRESS)
]


def _felt_from_iter(it: Iterator[bytes]):
    return int.from_bytes(next(it), "big")


def _uint256_from_iter(it: Iterator[bytes]):
    low = _felt_from_iter(it)
    high = _felt_from_iter(it)
    return (high << 128) + low


async def handle_transfer(block_number, event):
    if len(event.data) == 3:
        data_iter = iter(event.data)
        from_ = _felt_from_iter(data_iter)
        to = _felt_from_iter(data_iter)
        token_id = _felt_from_iter(data_iter)
    else:
        assert len(event.data) == 4
        data_iter = iter(event.data)
        from_ = _felt_from_iter(data_iter)
        to = _felt_from_iter(data_iter)
        token_id = _uint256_from_iter(data_iter)

    print(f'{block_number}\t{hex(token_id)}\t{hex(from_)} -> {hex(to)}')


async def main():
    async with IndexerManagerClient.insecure_channel(DEFAULT_APIBARA_SERVER_URL) as client:
        existing = await client.get_indexer(INDEXER_ID)
        if existing:
            await client.delete_indexer(INDEXER_ID)
        await client.create_indexer(INDEXER_ID, 61_000, FILTERS)

        print('connecting to server')
        server_stream, client = await client.connect_indexer()
        await client.connect_indexer(INDEXER_ID)
        print('stream started')
        async for message in server_stream:
            if isinstance(message, NewEvents):
                for event in message.events:
                    await handle_transfer(message.block_number, event)
                await client.ack_block(message.block_hash)


if __name__ == '__main__':
    asyncio.run(main())
