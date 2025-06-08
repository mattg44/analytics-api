from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.api.events import router as events_router
from src.api.db.session import init_db_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Code to run on startup
    init_db_session()
    yield
    # Code to run on shutdown
    # For example, closing database connections or cleaning up resources


app = FastAPI(lifespan=lifespan)
app.include_router(events_router, prefix="/api/events")


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


@app.get("/healthz")
def read_api_health():
    return {"status": "okey"}
