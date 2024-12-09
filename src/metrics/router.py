from typing import Annotated
from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.database import db_session
from src.metrics import schemas
from src.metrics.service import MetricService

current_router = APIRouter(prefix="/metrics")
memory_router = APIRouter(prefix="/memory")
cpu_router = APIRouter(prefix="/cpu")
disk_router = APIRouter(prefix="/disk")


@current_router.get(
    "/current-metrics/",
    response_model=schemas.MetricsOut,
    status_code=status.HTTP_200_OK
)
async def current_metrics() -> dict:
    metrics = await MetricService().current_metrics()
    return {
        "memory_usage_percent": metrics.memory_usage,
        "cpu_usage_percent": metrics.cpu_usage,
        "disk_space_total": metrics.disk_space_total,
        "disk_space_used": metrics.disk_space_used,
        "disk_usage": metrics.disk_usage
    }


@memory_router.get(
    "/minute-interval/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MaxMemoryPerMinute]
)
async def memory_usage_per_minute(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)]
):
    result = await MetricService().memory_usage_per_minute(db_session)
    return result


@memory_router.get(
    "/hour-interval/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MaxMemoryPerHour]
)
async def memory_usage_per_hour(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)]
):
    result = await MetricService().memory_usage_per_hour(db_session)
    return result


@cpu_router.get(
    "/minute-interval/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MaxCpuPerMinute]
)
async def cpu_usage_per_minute(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)]
):
    result = await MetricService().cpu_usage_per_minute(db_session)
    return result


@cpu_router.get(
    "/hour-interval/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MaxCpuPerHour]
)
async def cpu_usage_per_hour(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)]
):
    result = await MetricService().cpu_usage_per_hour(db_session)
    return result


@disk_router.get(
    "/minute-interval/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MaxDiskPerMinute]
)
async def disk_usage_per_minute(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)]
):
    result = await MetricService().disk_usage_per_minute(db_session)
    return result


@disk_router.get(
    "/hour-interval/",
    status_code=status.HTTP_200_OK,
    response_model=list[schemas.MaxDiskPerHour]
)
async def disk_usage_per_hour(
    db_session: Annotated[async_sessionmaker[AsyncSession], Depends(db_session)]
):
    result = await MetricService().disk_usage_per_hour(db_session)
    return result
