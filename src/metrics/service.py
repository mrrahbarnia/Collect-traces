import logging
import psutil # type: ignore
import asyncio
import sqlalchemy as sa

from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.metrics.models import Metric
from src.metrics.types import MetricsNamedTuple
from src.metrics.types import MetricId
from src.metrics.utils import send_email
from src.metrics.exceptions import DbConnException

logger = logging.getLogger("metrics")


class MetricService:
    def __init__(self):
        pass

    async def current_metrics(self) -> MetricsNamedTuple:
        """
        Collection of the system status at the present moment.
        """
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
        """
        Storing all metrics in db for analyzing purpose.
        """
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
    
    async def memory_usage_per_minute(
            self,
            db_session: async_sessionmaker[AsyncSession],
    ) -> sa.Sequence[sa.Row[tuple[Any, Any]]]:
        """
        Analyzing memory usage per minutes interval.
        """
        smtm = (
            sa.select(
                sa.func.date_trunc('minute', Metric.created_at).label("minute_interval"),
                sa.func.round(sa.cast(sa.func.avg(Metric.memory_usage), sa.Numeric), 2).label("memory_usage")
            )
            .select_from(Metric)
            .group_by(sa.text("1"))
            .order_by(sa.desc(sa.text("1")))
            .limit(10)
        )
        try:
            async with db_session.begin() as conn:
                return (await conn.execute(smtm)).all()
        except Exception as ex:
            logger.warning(ex)
            raise DbConnException
    
    async def memory_usage_per_hour(
            self,
            db_session: async_sessionmaker[AsyncSession],
    ) -> sa.Sequence[sa.Row[tuple[Any, Any]]]:
        """
        Analyzing memory usage per hours interval.
        """
        smtm = (
            sa.select(
                sa.func.date_trunc('hour', Metric.created_at).label("hour_interval"),
                sa.func.round(sa.cast(sa.func.avg(Metric.memory_usage), sa.Numeric), 2).label("memory_usage")
            )
            .select_from(Metric)
            .group_by(sa.text("1"))
            .order_by(sa.desc(sa.text("1")))
            .limit(10)
        )
        try:
            async with db_session.begin() as conn:
                return (await conn.execute(smtm)).all()
        except Exception as ex:
            logger.warning(ex)
            raise DbConnException

    async def cpu_usage_per_minute(
            self,
            db_session: async_sessionmaker[AsyncSession],
    ) -> sa.Sequence[sa.Row[tuple[Any, Any]]]:
        """
        Analyzing cpu usage per minutes interval.
        """
        smtm = (
            sa.select(
                sa.func.date_trunc('minute', Metric.created_at).label("minute_interval"),
                sa.func.round(sa.cast(sa.func.avg(Metric.cpu_usage), sa.Numeric), 2).label("cpu_usage")
            )
            .select_from(Metric)
            .group_by(sa.text("1"))
            .order_by(sa.desc(sa.text("1")))
            .limit(10)
        )
        try:
            async with db_session.begin() as conn:
                return (await conn.execute(smtm)).all()
        except Exception as ex:
            logger.warning(ex)
            raise DbConnException
    
    async def cpu_usage_per_hour(
            self,
            db_session: async_sessionmaker[AsyncSession],
    ) -> sa.Sequence[sa.Row[tuple[Any, Any]]]:
        """
        Analyzing cpu usage per hours interval.
        """
        smtm = (
            sa.select(
                sa.func.date_trunc('hour', Metric.created_at).label("hour_interval"),
                sa.func.round(sa.cast(sa.func.avg(Metric.cpu_usage), sa.Numeric), 2).label("cpu_usage")
            )
            .select_from(Metric)
            .group_by(sa.text("1"))
            .order_by(sa.desc(sa.text("1")))
            .limit(10)
        )
        try:
            async with db_session.begin() as conn:
                return (await conn.execute(smtm)).all()
        except Exception as ex:
            logger.warning(ex)
            raise DbConnException
    
    async def disk_usage_per_minute(
            self,
            db_session: async_sessionmaker[AsyncSession],
    ) -> sa.Sequence[sa.Row[tuple[Any, Any]]]:
        """
        Analyzing disk usage per minutes interval.
        """
        smtm = (
            sa.select(
                sa.func.date_trunc('minute', Metric.created_at).label("minute_interval"),
                sa.func.round(sa.cast(sa.func.avg(Metric.disk_usage), sa.Numeric), 2).label("disk_usage")
            )
            .select_from(Metric)
            .group_by(sa.text("1"))
            .order_by(sa.desc(sa.text("1")))
            .limit(10)
        )
        try:
            async with db_session.begin() as conn:
                return (await conn.execute(smtm)).all()
        except Exception as ex:
            logger.warning(ex)
            raise DbConnException
    
    async def disk_usage_per_hour(
            self,
            db_session: async_sessionmaker[AsyncSession],
    ) -> sa.Sequence[sa.Row[tuple[Any, Any]]]:
        """
        Analyzing disk usage per hour interval.
        """
        smtm = (
            sa.select(
                sa.func.date_trunc('hour', Metric.created_at).label("hour_interval"),
                sa.func.round(sa.cast(sa.func.avg(Metric.disk_usage), sa.Numeric), 2).label("disk_usage")
            )
            .select_from(Metric)
            .group_by(sa.text("1"))
            .order_by(sa.desc(sa.text("1")))
            .limit(10)
        )
        try:
            async with db_session.begin() as conn:
                return (await conn.execute(smtm)).all()
        except Exception as ex:
            logger.warning(ex)
            raise DbConnException
