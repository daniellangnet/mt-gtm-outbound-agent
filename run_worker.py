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
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    temporal_task_queue = os.getenv("TEMPORAL_TASK_QUEUE", "hello-task-queue")

    print("Connecting to Temporal Service")
    client = await Client.connect(temporal_address, namespace=temporal_namespace)

    print("Run worker")
    worker = Worker(client, task_queue=temporal_task_queue, workflows=[SayHello], activities=[say_hello])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
