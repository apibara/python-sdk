import asyncio
from decimal import Decimal
from typing import List

from grpc import ssl_channel_credentials
from grpc.aio import secure_channel

from apibara.protocol import StreamClient, StreamService
from apibara.protocol.proto.stream_pb2 import Cursor, Data, DataFinality
from apibara.starknet import Block, EventFilter, Filter, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.filter import StateUpdateFilter, StorageDiffFilter
from apibara.starknet.proto.starknet_pb2 import Event, Transaction
from apibara.starknet.proto.types_pb2 import FieldElement

ETH_DECIMALS = 18

_DEN = Decimal(10**ETH_DECIMALS)

FACTORY_ADDRESS = felt.from_hex(
    "0x00dad44c139a476c7a17fc8141e6db680e9abc9f56fe249a105094c44382c2fd"
)

# `PairCreated` selector.
# You can get this value either with starknet.py's `ContractFunction.get_selector`
# or from starkscan.
PAIR_CREATED_KEY = felt.from_hex(
    "0x19437bf1c5c394fc8509a2e38c9c72c152df0bac8be777d4fc8f959ac817189"
)

SWAP_KEY = felt.from_hex(
    "0xe316f0d9d2a3affa97de1d99bb2aac0538e2666d0d8545545ead241ef0ccab"
)


def to_decimal(amount: int) -> Decimal:
    return Decimal(amount) / _DEN


def build_filter(events: List[EventFilter]) -> Filter:
    filter = Filter()
    for event in events:
        filter.add_event(event)
    return filter


def from_uint256(low: FieldElement, high: FieldElement) -> int:
    return felt.to_int(low) + (felt.to_int(high) << 128)


class EventHandler:
    def __init__(self, client):
        self.client = client
        self.filters = [
            EventFilter()
            .with_from_address(FACTORY_ADDRESS)
            .with_keys([PAIR_CREATED_KEY])
        ]

        self.rescan_cursor = None

    async def reconfigure(self, cursor=None):
        if cursor is None:
            cursor = starknet_cursor(5980)
        await self.client.configure(
            filter=build_filter(self.filters).encode(),
            finality=DataFinality.DATA_STATUS_ACCEPTED,
            cursor=cursor,
            batch_size=1,
        )

    async def handle_batch(self, batch: Data):
        cursor = batch.cursor
        if self.rescan_cursor is not None:
            # reset to include all filters
            if cursor.order_key > self.rescan_cursor.order_key:
                await self.reconfigure(cursor)
                self.rescan_cursor = None

        block = Block()
        for batch in batch.data:
            block.ParseFromString(batch)

            for event_with_tx in block.events:
                event = event_with_tx.event
                tx = event_with_tx.transaction

                if event.keys[0] == PAIR_CREATED_KEY:
                    await self.handle_pair_created(cursor, tx, event)
                elif event.keys[0] == SWAP_KEY:
                    await self.handle_swap(cursor, tx, event)

    async def handle_pair_created(self, cursor: Cursor, tx: Transaction, event: Event):
        tx_hash = felt.to_hex(tx.meta.hash)

        token_0 = felt.to_hex(event.data[0])
        token_1 = felt.to_hex(event.data[1])
        pair = felt.to_hex(event.data[2])
        count = felt.to_int(event.data[3])
        print("New Pair")
        print(f"  Tx Hash: {tx_hash}")
        print(f"     Pair: {token_0}")
        print(f"  Token 0: {token_1}")
        print(f"  Token 1: {pair}")
        print(f"    Count: {count}")
        print()

        pair_filter = (
            EventFilter().with_from_address(event.data[2]).with_keys([SWAP_KEY])
        )

        # add new pair to the global filters
        self.filters.append(pair_filter)

        # rescan the current block for events matching the new pair
        self.rescan_cursor = cursor
        await self.client.configure(
            filter=build_filter([pair_filter]).encode(),
            finality=DataFinality.DATA_STATUS_ACCEPTED,
            cursor=cursor,
            batch_size=1,
        )

    async def handle_swap(self, cursor: Cursor, tx: Transaction, event: Event):
        tx_hash = felt.to_hex(tx.meta.hash)

        sender = felt.to_hex(event.data[0])
        amount_0_in = from_uint256(event.data[1], event.data[2])
        amount_1_in = from_uint256(event.data[3], event.data[4])
        amount_0_out = from_uint256(event.data[5], event.data[6])
        amount_1_out = from_uint256(event.data[7], event.data[8])
        dest = felt.to_hex(event.data[9])

        print("New Swap")
        print(f"   Tx Hash: {tx_hash}")
        print(f"    Sender: {sender}")
        print(f"      Dest: {dest}")
        print(f"   Amnt in: {amount_0_in} o {amount_1_in}")
        print(f"  Amnt out: {amount_0_out} o {amount_1_out}")
        print()


async def main():

    channel = secure_channel("mainnet.starknet.a5a.ch", ssl_channel_credentials())

    (client, stream) = StreamService(channel).stream_data()

    handler = EventHandler(client)

    await handler.reconfigure()

    async for message in stream:
        if message.data is not None:
            await handler.handle_batch(message.data)


if __name__ == "__main__":
    asyncio.run(main())
