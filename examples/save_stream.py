# This script shows how to save a stream to a file.
# This is useful to generate data for your tests.

import asyncio
import sys
from argparse import ArgumentParser
from decimal import Decimal

from grpc import ssl_channel_credentials
from grpc.aio import secure_channel
from google.protobuf.json_format import MessageToJson, Parse

from apibara.protocol import StreamService
from apibara.protocol.proto.stream_pb2 import DataFinality
from apibara.starknet import EventFilter, Filter, felt, Block
from apibara.starknet.cursor import starknet_cursor
from apibara.starknet.filter import StateUpdateFilter, StorageDiffFilter

# Notice that here we import the low-level, proto definition
# of filter.
from apibara.starknet.proto.filter_pb2 import Filter as ProtoFilter


def example_filter():
    address = felt.from_hex(
        "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
    )

    # `Transfer` selector.
    # You can get this value either with starknet.py's `ContractFunction.get_selector`
    # or from starkscan.
    transfer_key = felt.from_hex(
        "0x99cd8bde557814842a3121e8ddfd433a539b8c9f14bf31ebf108d12e6196e9"
    )

    filter = (
        Filter()
        .with_header(weak=True)
        .add_event(EventFilter().with_from_address(address).with_keys([transfer_key]))
        .with_state_update(
            StateUpdateFilter().add_storage_diff(
                StorageDiffFilter().with_contract_address(address)
            )
        )
        .to_proto()
    )

    print(MessageToJson(filter))


async def stream_data(args):
    with open(args.filter) as f:
        filter = Parse(f.read(), ProtoFilter()).SerializeToString()

    channel = secure_channel(args.stream_url, ssl_channel_credentials())
    (client, stream) = StreamService(channel).stream_data()

    finality = DataFinality.DATA_STATUS_ACCEPTED
    if args.finalized:
        finality = DataFinality.DATA_STATUS_FINALIZED

    cursor = None
    if args.start_block:
        cursor = starknet_cursor(args.start_block)

    await client.configure(
        filter=filter,
        finality=finality,
        batch_size=args.batch_size,
        cursor=cursor,
    )

    block = Block()
    async for message in stream:
        if message.data is not None:
            if message.data.end_cursor.order_key > args.end_block:
                return

            for batch in message.data.data:
                block.ParseFromString(batch)
                print(MessageToJson(block))


async def main(argv):
    parser = ArgumentParser()
    sub_parsers = parser.add_subparsers(dest="command")

    _example_parser = sub_parsers.add_parser(
        "example-filter", help="Print an example filter"
    )

    stream_parser = sub_parsers.add_parser("stream", help="Print an example filter")
    stream_parser.add_argument("filter", help="JSON file with the filter")
    stream_parser.add_argument("stream_url", help="URL of the stream")
    stream_parser.add_argument(
        "--start-block", help="Starting block number (exclusive)", type=int
    )
    stream_parser.add_argument(
        "--end-block", help="End block number (inclusive)", type=int, required=True
    )
    stream_parser.add_argument("--batch-size", help="Batch size", type=int, default=10)
    finality_group = stream_parser.add_mutually_exclusive_group()
    finality_group.add_argument(
        "--finalized", help="Stream finalized data", action="store_true"
    )
    finality_group.add_argument(
        "--accepted", help="Stream finalized data", action="store_true"
    )

    args = parser.parse_args(argv)

    if args.command == "example-filter":
        return example_filter()
    elif args.command == "stream":
        return await stream_data(args)
    else:
        return parser.print_help()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
