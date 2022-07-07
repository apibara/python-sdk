from typing import Any, List, Optional

import aiohttp

from apibara.rpc import RpcClient
from apibara.starknet.hash import get_selector_from_name


class StarkNetRpcClient(RpcClient):
    def __init__(self, url: Optional[str]) -> None:
        if url is None:
            url = "https://starknet-goerli.apibara.com"
        self._url = url

    async def _request(self, method: str, params: List[Any]):
        async with aiohttp.ClientSession(self._url) as session:
            data = {"id": 1, "jsonrpc": "2.0", "method": method, "params": params}
            async with session.post("/", json=data) as response:
                response = await response.json()
                if "result" in response:
                    return response["result"]
                raise RuntimeError(response["error"]["message"])

    async def get_block_by_hash(self, hash: bytes) -> dict:
        return await self._request(
            "starknet_getBlockByHash", ["0x" + hash.hex(), "TXN_HASH"]
        )

    async def get_block_by_number(self, number: int) -> dict:
        return await self._request(
            "starknet_getBlockByNumber", [hex(number), "TXN_HASH"]
        )

    async def call(self, address: bytes, method: str, params: List[Any]) -> dict:
        params = [
            {
                "contract_address": "0x" + address.hex(),
                "entry_point_selector": hex(get_selector_from_name(method)),
                "calldata": params,
            },
            "latest",
        ]
        return await self._request("starknet_call", params)
