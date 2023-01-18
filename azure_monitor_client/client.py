import hmac
import json
from base64 import b64decode, b64encode
from datetime import datetime
from hashlib import sha256
from typing import Any

from aiohttp import ClientSession


class AzureMonitorClient:
    def __init__(self, *, workspace_id: str, shared_key: str) -> None:
        self.workspace_id = workspace_id
        self.shared_key = shared_key

    @property
    def resource(self) -> str:
        return "/api/logs"

    @property
    def endpoint(self) -> str:
        return f"https://{self.workspace_id}.ods.opinsights.azure.com{self.resource}?api-version=2016-04-01"

    def _build_signature(self, payload: bytes, x_ms_date: str) -> str:
        hash_parts = [
            "POST",
            len(payload),
            "application/json",
            f"x-ms-date:{x_ms_date}",
            self.resource,
        ]
        hash_bytes = "\n".join(str(s) for s in hash_parts).encode("utf-8")
        key = b64decode(self.shared_key)
        hash = b64encode(hmac.new(key, hash_bytes, digestmod=sha256).digest()).decode(
            "utf-8"
        )
        return f"SharedKey {self.workspace_id}: {hash}"

    async def send(self, log_type: str, payload: dict[str, Any]) -> None:
        date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": self._build_signature(body, date),
            "Content-Type": "application/json",
            "Log-Type": log_type,
            "X-MS-Date": date,
        }
        async with ClientSession() as session:
            async with session.post(
                self.endpoint, data=body, headers=headers
            ) as response:
                response.raise_for_status()
