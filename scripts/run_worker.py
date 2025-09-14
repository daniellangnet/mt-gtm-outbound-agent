import asyncio
import uvicorn
from fastapi import FastAPI
from temporalio.worker import Worker

from activities import say_hello
from workflows import SayHello
from utils.temporal_utils import connect_temporal

app = FastAPI()

@app.get("/health/live")
async def live() -> dict:
    # If the server can answer, the process/event loop is alive
    return {"status": "ok"}

async def start_worker():
    print("Start worker in background")
    client, temporal_task_queue = await connect_temporal()

    async with Worker(client, task_queue=temporal_task_queue, workflows=[SayHello], activities=[say_hello]):
        print("Worker has connected to Temporal!")

        # Block forever; shutdown is handled by Fly sending a signal
        await asyncio.Event().wait()

async def main():
    asyncio.create_task(start_worker())

    # Start the HTTP server (FastAPI via uvicorn) on the same loop
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
