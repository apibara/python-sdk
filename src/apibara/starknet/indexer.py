from apibara.indexer.indexer import Indexer
from apibara.starknet.filter import Filter
from apibara.starknet.proto.starknet_pb2 import Block


class StarkNetIndexer(Indexer[Filter, Block]):
    def encode_filter(self, filter: Filter) -> bytes:
        return filter.encode()

    def decode_data(self, raw: bytes) -> Block:
        block = Block()
        block.ParseFromString(raw)
        return block
