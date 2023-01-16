import asyncio
import logging
import sys
from argparse import ArgumentParser
from typing import List, NamedTuple

from apibara.indexer import IndexerRunner, IndexerRunnerConfiguration, Info
from apibara.indexer.indexer import IndexerConfiguration
from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality
from apibara.starknet import EventFilter, Filter, StarkNetIndexer, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.proto.starknet_pb2 import Block

# Print apibara logs
root_logger = logging.getLogger("apibara")
# change to `logging.INFO` to print less information
root_logger.setLevel(logging.DEBUG)
root_logger.addHandler(logging.StreamHandler())

briqs_address = felt.from_hex(
    "0x01435498bf393da86b4733b9264a86b58a42b31f8d8b8ba309593e5c17847672"
)

# `Transfer` selector.
# You can get this value either with starknet.py's `ContractFunction.get_selector`
# or from starkscan.
transfer_key = felt.from_hex(
    "0x99cd8bde557814842a3121e8ddfd433a539b8c9f14bf31ebf108d12e6196e9"
)


class BriqIndexer(StarkNetIndexer):
    def indexer_id(self) -> str:
        return "starknet-example"

    def initial_configuration(self) -> Filter:
        # Return initial configuration of the indexer.
        return IndexerConfiguration(
            filter=Filter().add_event(
                EventFilter().with_from_address(briqs_address).with_keys([transfer_key])
            ),
            starting_cursor=starknet_cursor(10_000),
            finality=DataFinality.DATA_STATUS_FINALIZED,
        )

    async def handle_data(self, info: Info, data: Block):
        # Handle one block of data
        for event_with_tx in data.events:
            print(event_with_tx.event)

    async def handle_invalidate(self, _info: Info, _cursor: Cursor):
        raise ValueError("data must be finalized")


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
    await runner.run(BriqIndexer(), ctx={"network": "starknet-mainnet"})


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
