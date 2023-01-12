import apibara.starknet.proto.filter_pb2 as proto


class Filter:
    def __init__(self):
        self._inner = proto.Filter()

    def encode(self) -> bytes:
        return self._inner.SerializeToString()

    def with_header(self) -> "Filter":
        self._inner.header.CopyFrom(proto.HeaderFilter())
        return self

    def add_transaction(self, tx: "TransactionFilter") -> "Filter":
        self._inner.transactions.add(tx.encode())
        return self

    def add_event(self, ev: "EventFilter") -> "Filter":
        self._inner.events.add(ev.encode())
        return self

    def add_message(self, msg: "MessageFilter") -> "Filter":
        self._inner.messages.add(msg.encode())
        return self

    def with_state_update(self, state_update: "StateUpdateFilter") -> "Filter":
        self._inner.state_update.CopyFrom(state_update.encode())
        return self


class TransactionFilter:
    def encode(self) -> proto.TransactionFilter:
        pass


class EventFilter:
    def encode(self) -> proto.EventFilter:
        pass


class MessageFilter:
    def encode(self) -> proto.L2ToL1MessageFilter:
        pass


class StateUpdateFilter:
    def encode(self) -> proto.StateUpdateFilter:
        pass
