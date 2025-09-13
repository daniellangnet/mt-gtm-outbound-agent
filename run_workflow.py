import asyncio
import os
from dotenv import load_dotenv

from workflows import SayHello
from temporalio.client import Client

# Load environment variables from a .env file (if present)
load_dotenv()

async def main():
    temporal_address = os.getenv("TEMPORAL_ADDRESS", "localhost:7233")
    temporal_namespace = os.getenv("TEMPORAL_NAMESPACE", "default")
    temporal_task_queue = os.getenv("TEMPORAL_TASK_QUEUE", "hello-task-queue")

    print("Connecting to Temporal Service")
    client = await Client.connect(temporal_address, namespace=temporal_namespace)

    print("Executing workflow")
    result = await client.execute_workflow(SayHello.run, "Daniel", id="hello-workflow", task_queue=temporal_task_queue)

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
