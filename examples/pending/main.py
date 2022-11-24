# This example shows how to handle pending blocks.
import asyncio
import sys
from argparse import ArgumentParser
from typing import List, Tuple

from apibara import EventFilter, Info, NewBlock, NewEvents
from apibara.indexer.runner import IndexerRunner, IndexerRunnerConfiguration
from apibara.indexer.storage import Storage

indexer_id = "starknet-pending-example"
# eth token address
eth_address = "0x049d36570d4e46f48e99674bd3fcc84644ddd6b96f7c741b1562b82f9e004dc7"


def decode_transfer_event(data: List[bytes]) -> Tuple[int, int, int]:
    data = [int.from_bytes(b, "big") for b in data]
    from_addr = data[0]
    to_addr = data[1]
    low, high = data[2], data[3]
    amount = low + (high << 128)
    return from_addr, to_addr, amount


def short_hex_address(addr: int) -> str:
    """Returns the short hex representation of the given address."""
    addr = hex(addr)
    return f"{addr[:6]}...{addr[-4:]}"


def encode_int_as_bytes(n: int) -> bytes:
    """Encode an integer to bytes so that it can be stored in a db."""
    return n.to_bytes(32, "big", signed=True)


def decode_bytes_as_int(b: bytes) -> int:
    """Decodes an integer stored as bytes."""
    return int.from_bytes(b, "big", signed=True)


async def update_address_balance(storage: Storage, address: str, amount: int):
    address = encode_int_as_bytes(address)
    existing = await storage.find_one("balances", {"address": address})

    if existing is None:
        new_balance = amount
    else:
        balance = decode_bytes_as_int(existing["balance"])
        new_balance = balance + amount

    new_balance = encode_int_as_bytes(new_balance)
    await storage.find_one_and_replace(
        "balances",
        {"address": address},
        {"address": address, "balance": new_balance},
        upsert=True,
    )


async def update_balances(info: Info, block_events: NewEvents):
    balance_change = dict()
    for event in block_events.events:
        from_addr, to_addr, amount = decode_transfer_event(event.data)

        if from_addr not in balance_change:
            balance_change[from_addr] = 0
        balance_change[from_addr] -= amount

        if to_addr not in balance_change:
            balance_change[to_addr] = 0
        balance_change[to_addr] += amount

        await update_address_balance(info.storage, from_addr, -amount)
        await update_address_balance(info.storage, to_addr, amount)

        # also track transfer
        from_addr = encode_int_as_bytes(from_addr)
        to_addr = encode_int_as_bytes(to_addr)
        amount = encode_int_as_bytes(amount)
        await info.storage.insert_one(
            "transfers", {"sender": from_addr, "recipient": to_addr, "amount": amount}
        )


async def handle_events(info: Info, block_events: NewEvents):
    block_time = block_events.block.timestamp
    print(f"Handle block events: Block No. {block_events.block.number} - {block_time}")
    await update_balances(info, block_events)


async def handle_pending(info: Info, block_events: NewEvents):
    block_time = block_events.block.timestamp
    print(
        f"Handle pending block events: Block No. {block_events.block.number} - {block_time}"
    )
    await update_balances(info, block_events)


async def main(argv):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args(argv)

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            apibara_url="mainnet.starknet.stream.apibara.com:443",
            storage_url="mongodb://apibara:apibara@localhost:27017",
        ),
        reset_state=args.reset,
        indexer_id=indexer_id,
        new_events_handler=handle_events,
    )

    # Receive pending blocks every 5 seconds
    runner.add_pending_events_handler(handle_pending, interval_seconds=5)

    # Listen for ETH transfers, starting from a recent block.
    runner.add_event_filters(
        filters=[EventFilter.from_event_name(name="Transfer", address=eth_address)],
        index_from_block=1_000,
    )

    await runner.run()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
