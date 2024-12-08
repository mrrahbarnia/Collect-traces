import psutil # type: ignore
import asyncio

from collections import namedtuple

Metrics = namedtuple(
    "Metrics",
    ["cpu_usage", "memory_usage", "disk_space_total", "disk_space_used", "disk_usage"]
)


class MetricService:
    def __init__(self):
        pass

    async def current_metrics(self) -> Metrics:
        cpu_usage = await asyncio.to_thread(psutil.cpu_percent, interval=1)
        memory_info = await asyncio.to_thread(psutil.virtual_memory)
        disk_space = await asyncio.to_thread(psutil.disk_usage, "/")
        return Metrics(
            cpu_usage=cpu_usage,
            memory_usage=memory_info.percent,
            disk_space_total=disk_space.total,
            disk_space_used=disk_space.used,
            disk_usage=disk_space.percent
        )
