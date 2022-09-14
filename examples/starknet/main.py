import asyncio
import sys
from argparse import ArgumentParser
from typing import List, NamedTuple

from starknet_py.contract import (FunctionCallSerializer,
                                  identifier_manager_from_abi)

from apibara.legacy import (EventFilter, IndexerRunner,
                            IndexerRunnerConfiguration, Info, NewBlock,
                            NewEvents)

indexer_id = "starknet-example"
briqs_address = "0x0266b1276d23ffb53d99da3f01be7e29fa024dd33cd7f7b1eb7a46c67891c9d0"


# Use starknet.py to handle decoding the raw starknet events to
# a pythonic struct.
# In the future, Apibara will decode events server-side before sending
# to the indexer.
uint256_abi = {
    "name": "Uint256",
    "type": "struct",
    "size": 2,
    "members": [
        {"name": "low", "offset": 0, "type": "felt"},
        {"name": "high", "offset": 1, "type": "felt"},
    ],
}

transfer_abi = {
    "name": "Transfer",
    "type": "event",
    "keys": [],
    "outputs": [
        {"name": "from_address", "type": "felt"},
        {"name": "to_address", "type": "felt"},
        {"name": "token_id", "type": "Uint256"},
    ],
}

transfer_decoder = FunctionCallSerializer(
    abi=transfer_abi,
    identifier_manager=identifier_manager_from_abi([transfer_abi, uint256_abi]),
)


def decode_transfer_event(data: List[bytes]) -> NamedTuple:
    # Notice that in this example we are only indexing briqs
    # events. Some smart contracts on StarkNet use a felt to
    # encode the token_id.
    # In that case, need to update the code to check the number
    # of felts in the event's data (3 or 4) and use the appropriate
    # decoder.

    # starknet.py expects data to be a list of ints, so start
    # by converting bytes to that.
    data = [int.from_bytes(b, "big") for b in data]
    return transfer_decoder.to_python(data)


def encode_int_as_bytes(n: int) -> bytes:
    """Encode an integer to bytes so that it can be stored in a db."""
    return n.to_bytes(32, "big")


async def handle_events(info: Info, block_events: NewEvents):
    """Handle a group of briq's transfers grouped by block."""
    # Get information about the block so that all data can
    # be stored together with a block timestamp.
    block_time = block_events.block.timestamp
    print(f"Handle block events: Block No. {block_events.block.number} - {block_time}")

    for ev in block_events.events:
        print(ev.name)

    transfers = [
        {
            "event": decode_transfer_event(event.data),
            "transaction_hash": event.transaction_hash,
        }
        for event in block_events.events
    ]

    print("    Transfers decoded.")

    # Start by storing all transfers in the `transfers` collection.
    # The documents passed to the storage functions must be Python's
    # dictionaries, so start by converting to that.
    transfers_docs = [
        {
            "from_address": encode_int_as_bytes(tr["event"].from_address),
            "to_address": encode_int_as_bytes(tr["event"].to_address),
            "token_id": encode_int_as_bytes(tr["event"].token_id),
            "transaction_hash": tr["transaction_hash"],
            "timestamp": block_time,
        }
        for tr in transfers
    ]

    # Now store to the database.
    #
    # Apibara will automatically associate the current block number
    # to the data so that in case of chain reorganization data is
    # invalidated and state rolled back to the correct one.
    await info.storage.insert_many("transfers", transfers_docs)

    print("    Transfers stored.")

    # For each token, update the account that owns it.
    # Since a token may have been transferred multiple times in
    # the same block, we compute the final owner in Python and only
    # write this to the database.
    new_token_owner = dict()
    for transfer in transfers:
        new_token_owner[transfer["event"].token_id] = transfer["event"].to_address

    # Now store the new tokens state to the database.
    #
    # Notice that this calls does not delete the old data, but it
    # clamps the range of blocks in which its valid.
    #
    # For example, assume a token was minted at block 100 by 0xA,
    # the document looks like:
    #
    #   [100, None]   {"owner": "0xA"}
    #
    # Then at block 103 0xA transfers the token to 0xB, now the
    # documents are updated to be:
    #
    #   [100,  103]   {"owner": "0xA"}
    #   [103, None]   {"owner": "0xB"}
    #
    # These low level details are handled by the Apibara Server and
    # the SDK.
    for token_id, new_owner in new_token_owner.items():
        token_id = encode_int_as_bytes(token_id)
        # Use upsert to store the token if it's the first
        # time indexing it.
        await info.storage.find_one_and_replace(
            "tokens",
            {"token_id": token_id},
            {
                "token_id": token_id,
                "owner": encode_int_as_bytes(new_owner),
                "updated_at": block_time,
            },
            upsert=True,
        )

    print("    Owners updated.")


async def handle_block(info: Info, block: NewBlock):
    # Store the block information in the database.
    block = {
        "number": block.new_head.number,
        "hash": block.new_head.hash,
        "timestamp": block.new_head.timestamp.isoformat(),
    }
    await info.storage.insert_one("blocks", block)


async def main(argv):
    parser = ArgumentParser()
    parser.add_argument("--reset", action="store_true")
    args = parser.parse_args(argv)

    runner = IndexerRunner(
        config=IndexerRunnerConfiguration(
            apibara_url="goerli.starknet.stream.apibara.com:443",
            apibara_ssl=True,
            storage_url="mongodb://apibara:apibara@localhost:27017",
        ),
        reset_state=args.reset,
        network_name="starknet-goerli",
        indexer_id=indexer_id,
        new_events_handler=handle_events,
    )

    runner.add_block_handler(handle_block)

    # Create the indexer if it doesn't exist on the server,
    # otherwise it will resume indexing from where it left off.
    #
    # For now, this also helps the SDK map between human-readable
    # event names and StarkNet events.
    runner.create_if_not_exists(
        filters=[EventFilter.from_event_name(name="Transfer", address=briqs_address)],
        index_from_block=180_000,
    )

    await runner.run()


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1:]))
