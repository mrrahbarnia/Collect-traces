from pydantic import BaseModel, Field
from typing import Annotated

from src.metrics.types import (
    MemoryUsage,
    CpuUsage,
    DiskSpaceTotal,
    DiskSpaceUsed,
    DiskUsage
)


class MetricsOut(BaseModel):
    memory_usage_percent: Annotated[
        MemoryUsage, Field(serialization_alias="memoryUsagePercent")
    ]
    cpu_usage_percent: Annotated[
        CpuUsage, Field(serialization_alias="cpuUsagePercent")
    ]
    disk_space_total: Annotated[
        DiskSpaceTotal, Field(serialization_alias="diskSpaceTotal")
    ]
    disk_space_used: Annotated[
        DiskSpaceUsed, Field(serialization_alias="diskSpaceUsed")
    ]
    disk_usage: Annotated[DiskUsage, Field(serialization_alias="diskUsage")]
