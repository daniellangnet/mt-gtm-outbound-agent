import os
from typing import Tuple

from dotenv import load_dotenv
from temporalio.client import Client


def _bool_env(name: str, default: bool = False) -> bool:
    """Parse a boolean environment variable (true/false), case-insensitive.

    If the env var is missing, return the provided default.
    """
    val = os.getenv(name)
    if val is None:
        return default
    return val.lower() == "true"


async def connect_temporal() -> Tuple[Client, str]:
    """Create and return a Temporal client using environment variables.

    Returns a tuple of (client, task_queue).
    Expected environment variables:
      - TEMPORAL_ADDRESS
      - TEMPORAL_NAMESPACE
      - TEMPORAL_API_KEY
      - TEMPORAL_TASK_QUEUE
      - TEMPORAL_TLS ("true"/"false")
    """
    # Load environment variables from a .env file (if present)
    load_dotenv()

    temporal_address = os.getenv("TEMPORAL_ADDRESS")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE")
    temporal_api_key = os.getenv("TEMPORAL_API_KEY")
    temporal_task_queue = os.getenv("TEMPORAL_TASK_QUEUE")
    temporal_tls = _bool_env("TEMPORAL_TLS", False)

    print("Connecting to Temporal Service")
    client = await Client.connect(
        temporal_address,
        namespace=temporal_namespace,
        api_key=temporal_api_key,
        tls=temporal_tls,
    )

    return client, temporal_task_queue
