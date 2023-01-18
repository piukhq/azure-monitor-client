from base64 import b64encode
from datetime import datetime

from aioresponses import aioresponses

from azure_monitor_client import AzureMonitorClient


async def test_send_log_message() -> None:
    """
    Ensure no exceptions are raised when sending an event.
    """
    client = AzureMonitorClient(
        workspace_id="test-workspace-id",
        shared_key=b64encode(b"test-shared-key").decode(),
    )

    with aioresponses() as mock:
        mock.post(client.endpoint, status=200)

        await client.send(
            "TestEvent",
            {
                "test": True,
                "date": datetime.now().isoformat(),
                "value": 65.02,
            },
        )
