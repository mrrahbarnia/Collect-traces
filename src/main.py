import asyncio
import logging

from typing import AsyncGenerator
from fastapi import FastAPI
from logging.config import dictConfig
from contextlib import asynccontextmanager

from src.config import LogConfig, app_configs
from src.metrics import router as metrics_router
from src.metrics.schedular import clock_app

logger = logging.getLogger("root")


@asynccontextmanager
async def lifespan(_application: FastAPI) -> AsyncGenerator:
    dictConfig(LogConfig().model_dump())
    logger.info("App is running...")
    task = asyncio.create_task(clock_app.serve())

    yield

    try:
        task.cancel()
        await task
    except Exception as ex:
        logger.warning(ex)

app = FastAPI(**app_configs, lifespan=lifespan)

app.include_router(router=metrics_router.router, prefix="/metrics", tags=["metrics"])
