import asyncio
import sys
from argparse import ArgumentParser
from datetime import datetime
from typing import List

from hexbytes import HexBytes
from web3 import Web3
from web3._utils.events import get_event_data

from apibara import Client, IndexerRunner, Info, NewBlock, NewEvents
from apibara.indexer.runner import IndexerRunnerConfiguration
from apibara.model import EventFilter

indexer_id = "lens-protocol"

profile_created_abi = {
    "name": "ProfileCreated",
    "type": "event",
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "profileId", "type": "uint256"},
        {"indexed": True, "name": "creator", "type": "address"},
        {"indexed": True, "name": "to", "type": "address"},
        {"indexed": False, "name": "handle", "type": "string"},
        {"indexed": False, "name": "imageURI", "type": "string"},
        {"indexed": False, "name": "followModule", "type": "address"},
        {"indexed": False, "name": "followModuleReturnData", "type": "bytes"},
        {"indexed": False, "name": "followNFTURI", "type": "string"},
        {"indexed": False, "name": "timestamp", "type": "uint256"},
    ],
}

w3 = Web3()


def decode_profile_created(topics: List[bytes], data: bytes):
    log = {
        "logIndex": 0,
        "transactionIndex": 0,
        "transactionHash": "0x0",
        "address": "0x0",
        "blockHash": "0x0",
        "blockNumber": 0,
        "data": data,
        "topics": topics,
    }
    res = get_event_data(w3.codec, profile_created_abi, log)
    return res["args"]


async def handle_events(info: Info, block_events: NewEvents):
    print(f"Block {block_events.block.number} - {len(block_events.events)} events")

    for event in block_events.events:
        profile_created = decode_profile_created(event.topics, event.data)
        timestamp = datetime.fromtimestamp(profile_created.timestamp)
        print(f"   {event}")
        print(f"   {profile_created}")
        await info.storage.insert_one(
            "profiles",
            {
                "id": profile_created.profileId,
                "creator": bytes(HexBytes(profile_created.creator)),
                "to": bytes(HexBytes(profile_created.to)),
                "handle": profile_created.handle,
                "imageUri": profile_created.imageURI,
                "followModule": bytes(HexBytes(profile_created.followModule)),
                "followNFTURI": profile_created.followNFTURI,
                "timestamp": timestamp,
            },
        )


async def handle_block(info: Info, block: NewBlock):
    print(block)


async def main(args):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true", default=False)
    args = parser.parse_args()

    if args.reset:
        async with Client.connect() as client:
            existing = await client.indexer_client().get_indexer(indexer_id)
            if existing:
                await client.indexer_client().delete_indexer(indexer_id)
                print("Indexer deleted. Starting from beginning.")

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            storage_url="mongodb://apibara:apibara@localhost:27017"
        ),
        network_name="polygon",
        indexer_id=indexer_id,
        new_events_handler=handle_events,
    )

    runner.add_block_handler(handle_block)

    runner.create_if_not_exists(
        filters=[
            EventFilter.from_event_name(
                name="ProfileCreated(uint256,address,address,string,string,address,bytes,string,uint256)",
                address="0xDb46d1Dc155634FbC732f92E853b10B288AD5a1d",
            )
        ],
        index_from_block=30800000,
    )

    await runner.run()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
