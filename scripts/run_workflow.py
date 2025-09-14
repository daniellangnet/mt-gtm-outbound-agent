import asyncio

from workflows import SayHello
from utils.temporal_utils import connect_temporal


async def main():
    client, temporal_task_queue = await connect_temporal()

    print("Executing workflow")
    result = await client.execute_workflow(SayHello.run, "Daniel", id="hello-workflow", task_queue=temporal_task_queue)

    print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(main())
