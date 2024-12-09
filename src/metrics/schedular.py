import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncGenerator, Annotated
from aioclock import AioClock, Every, Depends
from contextlib import asynccontextmanager

from src.metrics.service import MetricService
from src.metrics.types import MetricsNamedTuple
from src.database import db_session

logger = logging.getLogger("metrics")


@asynccontextmanager
async def aioclock_lifespan(aio_clock: AioClock) -> AsyncGenerator[AioClock, None]:
    logger.info("Starting aioclock app...")
    yield aio_clock
    logger.info("Closing aioclock app...")

clock_app = AioClock(lifespan=aioclock_lifespan)


@clock_app.task(trigger=Every(seconds=10))
async def collect_metrics(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)],
) -> None:
    metrics: MetricsNamedTuple = await MetricService().current_metrics()
    # Persists metrics in db
    await MetricService().store_metrics(db_session, metrics)
