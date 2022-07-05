from typing import Any, List


class RpcClient:
    async def get_block_by_hash(self, hash: bytes) -> dict:
        pass

    async def get_block_by_number(self, number: int) -> dict:
        pass

    async def call(self, address: bytes, method: str, params: List[Any]) -> dict:
        pass
