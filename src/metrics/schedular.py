import logging

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from typing import AsyncGenerator, Annotated
from aioclock import AioClock, Every, Depends
from contextlib import asynccontextmanager

from src.metrics.service import MetricService
from src.metrics.types import MetricsNamedTuple
from src.database import db_session
from src.metrics.utils import send_email
from src.metrics.config import metric_config

logger = logging.getLogger("metrics")


@asynccontextmanager
async def aioclock_lifespan(aio_clock: AioClock) -> AsyncGenerator[AioClock, None]:
    """
    Schedular lifespan for working in background.
    """
    logger.info("Starting aioclock app...")
    yield aio_clock
    logger.info("Closing aioclock app...")

clock_app = AioClock(lifespan=aioclock_lifespan)


@clock_app.task(trigger=Every(seconds=20))
async def collect_metrics(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)],
) -> None:
    """
    Schedular for collecting metrics every 20 seconds,and store
    them in db. The maintainer can replace metric_config variables
    with his favorite maximum percentage to alerting admin user
    whenever system resources exceeds those.
    """
    metrics: MetricsNamedTuple = await MetricService().current_metrics()
    if metrics.cpu_usage > metric_config.MAX_CPU_PERCENT_ALERT:
        send_email(f"Cpu usage exceeds {metric_config.MAX_CPU_PERCENT_ALERT}%!")
        logger.warning(f"Cpu usage exceeds {metric_config.MAX_CPU_PERCENT_ALERT}%!")
    if metrics.memory_usage > metric_config.MAX_MEMORY_PERCENT_ALERT:
        send_email(f"Memory usage exceeds {metric_config.MAX_MEMORY_PERCENT_ALERT}%!")
        logger.warning(f"Memory usage exceeds {metric_config.MAX_MEMORY_PERCENT_ALERT}%!")
    if metrics.disk_usage > metric_config.MAX_DISK_PERCENT_ALERT:
        send_email(f"Disk usage exceeds {metric_config.MAX_DISK_PERCENT_ALERT}%!")
        logger.warning(f"Disk usage exceeds {metric_config.MAX_DISK_PERCENT_ALERT}%!")
    # Persists metrics in db
    await MetricService().store_metrics(db_session, metrics)
