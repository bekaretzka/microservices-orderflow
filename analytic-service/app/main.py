import asyncio
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from app.consumer import consume_evenets
from app.database import mongodb_client, events_collection


@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(consume_evenets)

    try:
        yield
    finally:
        task.cancel()

        with suppress(asyncio.CancelledError):
            await task

        await mongodb_client.clos()

app = FastAPI(lifespan=lifespan)


@app.get("/events")
async def get_events(limit: int = 20):
    query = events_collection.find().sort("created_at", -1).limit(limit)
    return query.to_list(limit)