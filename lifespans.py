from concurrent.futures import ThreadPoolExecutor
import logging
import os
from contextlib import asynccontextmanager
import contextlib
import threading
from typing import cast
from decouple import config
from fastapi import FastAPI
from mongoengine import connect, disconnect

logger = logging.getLogger(__name__)


@asynccontextmanager
async def mongodb_lifespan(app: FastAPI):
    MONGODB_URI = f"{config('MONGO_URI')}{config('DB_NAME')}"
    MONGODB_DATABASE_ALIAS = cast(str, config("DB_NAME"))
    connect(host=MONGODB_URI, alias=MONGODB_DATABASE_ALIAS)
    logger.info(
        f"Connected to MongoDB => DB_NAME :  {MONGODB_DATABASE_ALIAS} || (Process ID: {os.getpid()})"
    )
    try:
        yield
    finally:
        disconnect(alias=MONGODB_DATABASE_ALIAS)
        logger.info(f"Disconnected from MongoDB (Process ID: {os.getpid()})")


class Lifespans:
    def __init__(self, lifespans) -> None:
        self.lifespans = lifespans

    @asynccontextmanager
    async def __manage_lifespan(self, app: FastAPI):
        async with contextlib.AsyncExitStack() as exit_stack:
            for lifespan in self.lifespans:
                await exit_stack.enter_async_context(lifespan(app))
            yield

    def __call__(self, app: FastAPI):
        self.app = app
        return self.__manage_lifespan(app)
