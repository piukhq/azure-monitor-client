# Azure Monitor Client

A simple async client for the [Azure Monitor Data Collector API](https://learn.microsoft.com/en-us/azure/azure-monitor/logs/data-collector-api?tabs=python).

## Minimal Usage Example

```python
from datetime import datetime
from uuid import uuid4
import asyncio
import json

from azure_monitor_client import AzureMonitorClient

client = AzureMonitorClient(
    workspace_id=WORKSPACE_ID,
    shared_key=SHARED_KEY
)

async def send_event() -> None:
    # This is just an example of the kind of data you can send.
    # None of these fields are required.
    # For more information on data types, see:
    # https://www.stefanroth.net/2018/05/08/azure-log-analytics-get-data-types/
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "record_uid": str(uuid()),
        "active": True,
        "fields": json.dumps({
            "name": "Jackie Welles",
            "age": 30,
        })
    }

    await client.send("AuditLog", payload)

asyncio.run(send_event())
```

