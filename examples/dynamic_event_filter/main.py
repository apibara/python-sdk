import asyncio
import sys
from argparse import ArgumentParser
from typing import List, NamedTuple

from starknet_py.contract import FunctionCallSerializer, identifier_manager_from_abi

from apibara import EventFilter, Info, NewBlock, NewEvents
from apibara.indexer.runner import IndexerRunner, IndexerRunnerConfiguration
from apibara.model import BlockHeader, StarkNetEvent


indexer_id = "jediswap-testnet"
factory_address = "0x06c872d0696e7bf45735239393774f51455e3bdb08760a0dc76cd7c8688cfd60"

uint256_abi = {
    "name": "Uint256",
    "type": "struct",
    "size": 2,
    "members": [
        {"name": "low", "offset": 0, "type": "felt"},
        {"name": "high", "offset": 1, "type": "felt"},
    ],
}

pair_created_abi = {
    "name": "pair_created",
    "type": "event",
    "keys": [],
    "outputs": [
        {"name": "token0", "type": "felt"},
        {"name": "token1", "type": "felt"},
        {"name": "pair", "type": "felt"},
        {"name": "total_pairs", "type": "felt"},
    ],
}

sync_abi = {
    "name": "Sync",
    "type": "event",
    "keys": [],
    "outputs": [
        {"name": "reserve0", "type": "Uint256"},
        {"name": "reserve1", "type": "Uint256"},
    ],
}

swap_abi = {
    "name": "Swap",
    "type": "event",
    "keys": [],
    "outputs": [
        {"name": "sender", "type": "felt"},
        {"name": "amount0In", "type": "Uint256"},
        {"name": "amount1In", "type": "Uint256"},
        {"name": "amount0Out", "type": "Uint256"},
        {"name": "amount1Out", "type": "Uint256"},
        {"name": "to", "type": "felt"},
    ],
}

pair_created_decoder = FunctionCallSerializer(
    abi=pair_created_abi,
    identifier_manager=identifier_manager_from_abi([pair_created_abi]),
)

sync_decoder = FunctionCallSerializer(
    abi=sync_abi,
    identifier_manager=identifier_manager_from_abi([uint256_abi, sync_abi]),
)

swap_decoder = FunctionCallSerializer(
    abi=swap_abi,
    identifier_manager=identifier_manager_from_abi([uint256_abi, swap_abi]),
)


def decode_event(decoder: FunctionCallSerializer, data: List[bytes]):
    # starknet.py requires data to be int, not bytes
    return decoder.to_python([int.from_bytes(d, "big") for d in data])


async def handle_pair_created(info: Info, block: BlockHeader, event: StarkNetEvent):
    pair_created = decode_event(pair_created_decoder, event.data)
    print(f"PairCreated(pair=0x{hex(pair_created.pair)})")

    doc = {
        "pair": pair_created.pair.to_bytes(32, "big"),
        "token0": pair_created.token0.to_bytes(32, "big"),
        "token1": pair_created.token1.to_bytes(32, "big")
    }
    await info.storage.insert_one("pairs", doc)

    # Start tracking events from pair contract
    info.add_event_filters(filters=[
        EventFilter.from_event_name("Swap", address=pair_created.pair),
        EventFilter.from_event_name("Sync", address=pair_created.pair),
    ])


async def handle_sync(info: Info, block: BlockHeader, event: StarkNetEvent):
    sync = decode_event(sync_decoder, event.data)
    print(f"Sync({sync.reserve0}, {sync.reserve1})")


async def handle_swap(info: Info, block: BlockHeader, event: StarkNetEvent):
    swap = decode_event(swap_decoder, event.data)
    print(f"Swap(0x{hex(swap.sender)}, 0x{hex(swap.to)})")


async def handle_events(info: Info, block_events: NewEvents):
    for event in block_events.events:
        if event.name == "pair_created":
            await handle_pair_created(info, block_events.block, event)
        elif event.name == 'Sync':
            await handle_sync(info, block_events.block, event)
        elif event.name == 'Swap':
            await handle_swap(info, block_events.block, event)


async def handle_block(info: Info, block: NewBlock):
    pass


async def main(argv):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args(argv)

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            apibara_url="goerli.starknet.stream.apibara.com:443",
            storage_url="mongodb://apibara:apibara@localhost:27017",
        ),
        reset_state=args.reset,
        indexer_id=indexer_id,
        new_events_handler=handle_events,
    )

    runner.set_context({
        "network": "starknet-goerli"
    })

    # runner.add_block_handler(handle_block)

    # Add a filter on the factory to detect when pairs are created.
    runner.add_event_filters(
        filters=[
            EventFilter.from_event_name(name="pair_created", address=factory_address)],
        index_from_block=255_650,
    )

    await runner.run()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
