import asyncio

from temporalio.worker import Worker

from activities import say_hello
from workflows import SayHello
from utils.temporal_utils import connect_temporal


async def main():
    client, temporal_task_queue = await connect_temporal()

    print("Run worker")
    worker = Worker(client, task_queue=temporal_task_queue, workflows=[SayHello], activities=[say_hello])
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
