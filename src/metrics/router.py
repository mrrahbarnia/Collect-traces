from fastapi import APIRouter, status

from src.metrics.service import MetricService
from src.metrics.schemas import MetricsOut

router = APIRouter()


@router.get(
    "/current-metrics/",
    response_model=MetricsOut,
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
