from typing import NewType

MetricId = NewType("MetricId", int)
MemoryUsage = NewType("MemoryUsage", float)
CpuUsage = NewType("CpuUsage", float)
DiskSpaceTotal = NewType("DiskSpaceTotal", int)
DiskSpaceUsed = NewType("DiskSpaceUsed", int)
DiskUsage = NewType("DiskUsage", float)
