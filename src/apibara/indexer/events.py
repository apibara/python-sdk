import base64
from dataclasses import dataclass
from typing import Any, List, Optional

from starknet_py.contract import ContractFunction

from apibara.model import EventFilter, StarkNetEvent


class EventMatcher:
    """This class is used to extract events (according to some filters) from a StarkNet block."""

    def __init__(self, filters: List[EventFilter]) -> None:
        self._compile_and_replace_filters(filters)

    def find_events_in_block(self, block: Any) -> List[StarkNetEvent]:
        """Returns all events contained in `block` matching the current filters."""
        matched_events = []
        log_index = 0
        transactions = block.get("transactions", [])
        for receipt in block.get("transaction_receipts", []):
            tx = transactions[int(receipt.get("transaction_index", 0))]
            events = receipt.get("events", [])
            for event in events:
                event_name, matched = self._find_filter_matching_event(event)
                if matched:
                    tx_hash = _transaction_hash(tx)
                    event = StarkNetEvent.from_proto(
                        event, log_index, event_name, tx_hash
                    )
                    matched_events.append(event)
                log_index += 1
        return matched_events

    def replace_filters(self, filters: List[EventFilter]):
        """Replaces the current set of filters."""
        self._compile_and_replace_filters(filters)

    def merge(self, other: "EventMatcher") -> "EventMatcher":
        """Joins two matchers together into a new one."""
        new_filters = _unique_event_filters(self._filters + other._filters)
        return EventMatcher(new_filters)

    def _compile_and_replace_filters(self, filters: List[EventFilter]):
        self._compiled_filters = [
            CompiledEventFilter.from_event_filter(f) for f in filters
        ]
        self._filters = filters

    def _find_filter_matching_event(self, event):
        for filter in self._compiled_filters:
            if filter.matches(event):
                return filter.name, True
        return None, False


@dataclass
class CompiledEventFilter:
    name: str
    keys: List[bytes]
    address: Optional[bytes]

    @classmethod
    def from_event_filter(cls, filter: EventFilter):
        address = None
        if filter.address is not None:
            address = filter.address.ljust(32, b"\0")

        return CompiledEventFilter(
            name=filter.signature,
            keys=[ContractFunction.get_selector(filter.signature).to_bytes(32, "big")],
            address=address,
        )

    def matches(self, event):
        if "keys" not in event:
            return False

        if self.address is not None and "from_address" in event:
            event_address = base64.b64decode(event["from_address"]).ljust(32, b"\0")
            if event_address != self.address:
                return False

        event_keys = [base64.b64decode(k).ljust(32, b"\0") for k in event["keys"]]

        return event_keys == self.keys


def _transaction_hash(tx) -> bytes:
    common = None
    if "invoke" in tx:
        common = tx["invoke"]["common"]
    elif "deploy" in tx:
        common = tx["deploy"]["common"]
    elif "deploy_account" in tx:
        common = tx["deploy_account"]["common"]
    elif "declare" in tx:
        common = tx["declare"]["common"]
    elif "l1_handler" in tx:
        common = tx["l1_handler"]["common"]
    else:
        raise RuntimeError("unknown transaction type")
    return base64.b64decode(common["hash"])


def _unique_event_filters(filters: List[EventFilter]) -> List[EventFilter]:
    return list(set(filters))
