import asyncio
import logging
import os
import sys
from argparse import ArgumentParser
from typing import List, NamedTuple

from apibara.indexer import IndexerRunner, IndexerRunnerConfiguration, Info
from apibara.indexer.indexer import IndexerConfiguration
from apibara.protocol.proto.stream_pb2 import Cursor, DataFinality
from apibara.starknet import EventFilter, Filter, StarkNetIndexer, felt
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.proto.starknet_pb2 import Block

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")

# Print apibara logs
root_logger = logging.getLogger("apibara")
# change to `logging.DEBUG` to print more information
root_logger.setLevel(logging.INFO)
root_logger.addHandler(logging.StreamHandler())

# Application logs
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())

eth_address = felt.from_hex(
    "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
)

# `Transfer` selector.
# You can get this value either with starknet.py's `ContractFunction.get_selector`
# or from starkscan.
transfer_key = felt.from_hex(
    "0x99cd8bde557814842a3121e8ddfd433a539b8c9f14bf31ebf108d12e6196e9"
)


class TokenIndexer(StarkNetIndexer):
    def indexer_id(self) -> str:
        return "starknet-example"

    def initial_configuration(self) -> Filter:
        # Return initial configuration of the indexer.
        return IndexerConfiguration(
            filter=Filter()
            .with_header(weak=True)
            .add_event(
                EventFilter()
                .with_from_address(eth_address)
                .with_keys([transfer_key])
                .with_include_receipt(False)
                .with_include_transaction(True)
            ),
            starting_cursor=starknet_cursor(18_000),
            finality=DataFinality.DATA_STATUS_PENDING,
        )

    async def handle_data(self, info: Info, data: Block):
        self._handle_block(data, is_pending=False)

    async def handle_pending_data(self, info: Info, data: Block):
        self._handle_block(data, is_pending=True)

    async def handle_invalidate(self, _info: Info, cursor: Cursor):
        print(f"Chain reorganization {cursor}")

    def _handle_block(self, data: Block, is_pending: bool):
        block_number = data.header.block_number

        if is_pending:
            block_hash = "(pending)"
        else:
            block_hash = data.header.block_hash
            block_hash = f"({felt.to_hex(block_hash)})"

        logger.info(f"Block #{block_number} {block_hash}")
        for event_with_tx in data.events:
            event = event_with_tx.event
            transaction = event_with_tx.transaction

            tx_hash = transaction.meta.hash
            src = felt.to_hex(event.data[0])[:6]
            dest = felt.to_hex(event.data[1])[:6]
            event_id = f"{felt.to_hex(tx_hash)}_{event.index}"
            print(f"  Transfer from {src}... to {dest}... ({event_id})")


async def main(argv):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args(argv)

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            stream_url="sepolia.starknet.a5a.ch:443",
            storage_url="mongodb://apibara:apibara@localhost:27017",
            token=AUTH_TOKEN,
        ),
        # Increase max message size because ETH Transfer events
        # produce a lot of data per block.
        client_options=[
            ("grpc.max_send_message_length", 256 * 1024 * 1024),
            ("grpc.max_receive_message_length", 256 * 1024 * 1024),
        ],
        reset_state=args.reset,
    )

    await runner.run(TokenIndexer())


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
