import asyncio
import os
from dotenv import load_dotenv

from temporalio.client import Client
from temporalio.worker import Worker

from activities import say_hello
from workflows import SayHello

# Load environment variables from a .env file (if present)
load_dotenv()

async def main():
    temporal_address = os.getenv("TEMPORAL_ADDRESS")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE")
    temporal_api_key = os.getenv("TEMPORAL_API_KEY")
    temporal_task_queue = os.getenv("TEMPORAL_TASK_QUEUE")
    temporal_tls = os.getenv("TEMPORAL_TLS", "false").lower() == "true"

    print("Connecting to Temporal Service")
    client = await Client.connect(
        temporal_address,
        namespace=temporal_namespace,
        api_key=temporal_api_key,
        tls=temporal_tls
    )

    print("Run worker")
    worker = Worker(client, task_queue=temporal_task_queue, workflows=[SayHello], activities=[say_hello])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
