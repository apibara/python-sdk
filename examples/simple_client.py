import asyncio
import os
from decimal import Decimal

from grpc import ssl_channel_credentials
from grpc.aio import secure_channel

from apibara.protocol import StreamAddress, StreamService, credentials_with_auth_token
from apibara.protocol.proto.stream_pb2 import DataFinality
from apibara.starknet import Block, EventFilter, Filter, felt, starknet_cursor
from apibara.starknet.filter import StateUpdateFilter, StorageDiffFilter

ETH_DECIMALS = 18

_DEN = Decimal(10**ETH_DECIMALS)

AUTH_TOKEN = os.environ.get("AUTH_TOKEN")


def to_decimal(amount: int) -> Decimal:
    return Decimal(amount) / _DEN


async def main():
    address = felt.from_hex(
        "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"
    )

    # `Transfer` selector.
    # You can get this value either with starknet.py's `ContractFunction.get_selector`
    # or from starkscan.
    transfer_key = felt.from_hex(
        "0x99cd8bde557814842a3121e8ddfd433a539b8c9f14bf31ebf108d12e6196e9"
    )

    channel = secure_channel(
        StreamAddress.StarkNet.Mainnet,
        credentials_with_auth_token(AUTH_TOKEN, ssl_channel_credentials()),
    )

    (client, stream) = StreamService(channel).stream_data()

    filter = (
        Filter()
        .with_header(weak=False)
        .add_event(
            EventFilter()
            .with_from_address(address)
            .with_keys([transfer_key])
            .with_include_receipt(False)
            .with_include_transaction(True)
        )
        .encode()
    )

    print("sending configuration")
    await client.configure(
        filter=filter,
        finality=DataFinality.DATA_STATUS_ACCEPTED,
        batch_size=1,
        cursor=starknet_cursor(300_000),
    )

    print("starting stream")
    block = Block()
    async for message in stream:
        if message.data is None:
            print(message)
            continue
        else:
            for batch in message.data.data:
                block.ParseFromString(batch)
                num_events = len(block.events)

                print(
                    f"B {block.header.block_number} / {felt.to_hex(block.header.block_hash)} ({num_events} events)"
                )

                for event_with_tx in block.events:
                    event = event_with_tx.event
                    tx = event_with_tx.transaction

                    tx_hash = felt.to_hex(tx.meta.hash)

                    from_addr = felt.to_hex(event.data[0])
                    to_addr = felt.to_hex(event.data[1])
                    amount = felt.to_int(event.data[2]) + (
                        felt.to_int(event.data[3]) << 128
                    )
                    amount = to_decimal(amount)

                    print(f"  T {from_addr} => {to_addr}")
                    print(f"    Amount: {amount} ETH")
                    print(f"    Tx Hash: {tx_hash}")
                    print()


if __name__ == "__main__":
    asyncio.run(main())
