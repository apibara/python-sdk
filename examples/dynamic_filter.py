import asyncio
import logging
import sys
from argparse import ArgumentParser
from decimal import Decimal
from typing import List

from grpc import ssl_channel_credentials
from grpc.aio import secure_channel

from apibara.indexer import IndexerRunner, IndexerRunnerConfiguration, Info
from apibara.indexer.indexer import IndexerConfiguration
from apibara.protocol.proto.stream_pb2 import Cursor, Data, DataFinality
from apibara.starknet import Block, EventFilter, Filter, StarkNetIndexer, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.filter import StateUpdateFilter, StorageDiffFilter
from apibara.starknet.proto.starknet_pb2 import Event, Transaction
from apibara.starknet.proto.types_pb2 import FieldElement

# Print apibara logs
root_logger = logging.getLogger("apibara")
# change to `logging.DEBUG` to print more information
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler())

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

SYNC_KEY = felt.from_hex(
    "0xe14a408baf7f453312eec68e9b7d728ec5337fbdf671f917ee8c80f3255232"
)


def to_decimal(amount: int) -> Decimal:
    return Decimal(amount) / _DEN


def build_filter(events: List[EventFilter]) -> Filter:
    filter = Filter()
    for event in events:
        filter.add_event(event)
    return filter


def shorten_addr(addr: str) -> str:
    return addr[:6] + "..." + addr[-4:]


def from_uint256(low: FieldElement, high: FieldElement) -> int:
    return felt.to_int(low) + (felt.to_int(high) << 128)


class DexIndexer(StarkNetIndexer):
    def indexer_id(self) -> str:
        return "dynamic-filter-example"

    def initial_configuration(self) -> Filter:
        # Return initial configuration of the indexer.
        return IndexerConfiguration(
            filter=Filter()
            .with_header(weak=True)
            .add_event(
                EventFilter()
                .with_from_address(FACTORY_ADDRESS)
                .with_keys([PAIR_CREATED_KEY])
            ),
            starting_cursor=starknet_cursor(5980),
            finality=DataFinality.DATA_STATUS_ACCEPTED,
        )

    async def handle_data(self, info: Info, block: Block):
        print(
            f"Block {block.header.block_number}/0x{felt.to_hex(block.header.block_hash)}"
        )

        for event_with_tx in block.events:
            event = event_with_tx.event
            tx = event_with_tx.transaction

            if event.keys[0] == PAIR_CREATED_KEY:
                await self.handle_pair_created(info.cursor, tx, event)
            elif event.keys[0] == SWAP_KEY:
                await self.handle_swap(info.cursor, tx, event)
            elif event.keys[0] == SYNC_KEY:
                await self.handle_sync(info.cursor, tx, event)

    async def handle_pair_created(self, cursor: Cursor, tx: Transaction, event: Event):
        tx_hash = felt.to_hex(tx.meta.hash)

        token_0 = felt.to_hex(event.data[0])
        token_1 = felt.to_hex(event.data[1])
        pair = felt.to_hex(event.data[2])
        count = felt.to_int(event.data[3])
        print(f"  PairCreated({shorten_addr(token_0)}, {shorten_addr(token_1)}, {shorten_addr(pair)}, {count}) @ {tx_hash}")

        # Add the pair to the tracked pairs.
        self.update_filter(
            Filter()
            .with_header(weak=True)
            .add_event(
                EventFilter().with_from_address(event.data[2]).with_keys([SWAP_KEY])
            )
            .add_event(
                EventFilter().with_from_address(event.data[2]).with_keys([SYNC_KEY])
            )
        )

    async def handle_swap(self, cursor: Cursor, tx: Transaction, event: Event):
        tx_hash = felt.to_hex(tx.meta.hash)

        sender = felt.to_hex(event.data[0])
        amount_0_in = from_uint256(event.data[1], event.data[2])
        amount_1_in = from_uint256(event.data[3], event.data[4])
        amount_0_out = from_uint256(event.data[5], event.data[6])
        amount_1_out = from_uint256(event.data[7], event.data[8])
        dest = felt.to_hex(event.data[9])

        print(f"  Swap({shorten_addr(sender)}, {amount_0_in}, {amount_1_in}, {amount_0_out}, {amount_1_out}, {shorten_addr(dest)}) @ {tx_hash}")

    async def handle_sync(self, cursor: Cursor, tx: Transaction, event: Event):
        tx_hash = felt.to_hex(tx.meta.hash)

        reserve_0 = from_uint256(event.data[0], event.data[1])
        reserve_1 = from_uint256(event.data[2], event.data[3])

        print(f"  Sync({reserve_0}, {reserve_1}) @ {tx_hash}")


async def main(argv):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args(argv)

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            stream_url="mainnet.starknet.a5a.ch:443",
            storage_url="mongodb://apibara:apibara@localhost:27017",
        ),
        reset_state=args.reset,
    )

    # ctx can be accessed by the callbacks in `info`.
    await runner.run(DexIndexer())


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
