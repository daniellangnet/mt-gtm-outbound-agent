import asyncio
from fastapi import FastAPI, Response
from temporalio.worker import Worker
from temporalio.client import Client

from activities import say_hello
from workflows import SayHello
from utils.temporal_utils import connect_temporal

app = FastAPI()
ready = asyncio.Event()   # flipped when we're confident the worker is ready
client: Client | None = None

@app.get("/health/live")
async def live() -> dict:
    # If the server can answer, the process/event loop is alive
    return {"status": "ok"}

@app.get("/health/ready")
async def readyz():
    if not ready.is_set():
        return {"status": "starting"}
    try:
        await client.service_client.check_health()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "temporal_unreachable", "detail": str(e)}

async def start_worker():
    print("Start worker in background")
    global client
    client, temporal_task_queue = await connect_temporal()

    async with Worker(client, task_queue=temporal_task_queue, workflows=[SayHello], activities=[say_hello]):
        print("Worker has connected to Temporal!")
        # If we got here, the worker has connected and started pollers
        ready.set()
        # Block forever; shutdown is handled by Fly sending a signal
        await asyncio.Event().wait()

async def main():
    asyncio.create_task(start_worker())

    # Start the HTTP server (FastAPI via uvicorn) on the same loop
    import uvicorn
    config = uvicorn.Config(app, host="0.0.0.0", port=8080, loop="asyncio")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
