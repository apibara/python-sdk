import asyncio

from grpc import ssl_channel_credentials
from grpc.aio import secure_channel

from apibara.protocol import StreamService
from apibara.protocol.proto.stream_pb2 import DataFinality
from apibara.starknet import felt, Filter


async def main():
    address = felt.from_hex(
        '0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7'
    )

    channel = secure_channel(
        "mainnet.starknet.a5a.ch",
        ssl_channel_credentials()
    )

    (client, stream) = StreamService(channel).stream_data()

    filter = Filter().with_header().encode()

    await client.configure(
        filter=filter,
        finality=DataFinality.DATA_STATUS_FINALIZED,
        batch_size=10,
    )

    async for xxx in stream:
        print(xxx.data)


if __name__ == "__main__":
    asyncio.run(main())
