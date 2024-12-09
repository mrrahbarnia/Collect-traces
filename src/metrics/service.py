import logging
import psutil # type: ignore
import asyncio
import sqlalchemy as sa

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.metrics.models import Metric
from src.metrics.types import MetricsNamedTuple
from src.metrics.types import MetricId
from src.metrics.utils import send_email

logger = logging.getLogger("metrics")


class MetricService:
    def __init__(self):
        pass

    async def current_metrics(self) -> MetricsNamedTuple:
        cpu_usage = await asyncio.to_thread(psutil.cpu_percent, interval=1)
        memory_info = await asyncio.to_thread(psutil.virtual_memory)
        disk_space = await asyncio.to_thread(psutil.disk_usage, "/")
        return MetricsNamedTuple(
            cpu_usage=cpu_usage,
            memory_usage=memory_info.percent,
            disk_space_total=disk_space.total,
            disk_space_used=disk_space.used,
            disk_usage=disk_space.percent
        )

    async def store_metrics(
            self,
            db_session: async_sessionmaker[AsyncSession],
            metrics: MetricsNamedTuple
    ) -> None:
        smtm = sa.insert(Metric).values(
            {
                Metric.memory_usage: metrics.memory_usage,
                Metric.cpu_usage: metrics.cpu_usage,
                Metric.disk_space_total: metrics.disk_space_total,
                Metric.disk_space_used: metrics.disk_space_used,
                Metric.disk_usage: metrics.disk_usage
            }
        ).returning(Metric.id)
        async with db_session.begin() as conn:
            metric_id: MetricId | None = await conn.scalar(smtm)
            if not metric_id:
                logger.warning("Check db connection...")
                send_email(content="Check db connection...")
