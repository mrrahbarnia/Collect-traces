from typing import NewType, NamedTuple

MetricId = NewType("MetricId", int)
MemoryUsage = NewType("MemoryUsage", float)
CpuUsage = NewType("CpuUsage", float)
DiskSpaceTotal = NewType("DiskSpaceTotal", int)
DiskSpaceUsed = NewType("DiskSpaceUsed", int)
DiskUsage = NewType("DiskUsage", float)

class MetricsNamedTuple(NamedTuple):
    cpu_usage: float
    memory_usage: float
    disk_space_total: int
    disk_space_used: int
    disk_usage: float