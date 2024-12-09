"""
Serializing data with awesome pydantic :)
"""
from pydantic import BaseModel, Field, field_validator
from typing import Annotated
from datetime import datetime, time

from src.metrics.utils import convert_datetime_to_time

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


class MemoryBase(BaseModel):
    memory_usage: Annotated[float, Field(serialization_alias="memoryUsage")]


class MaxMemoryPerMinute(MemoryBase):
    minute_interval: Annotated[datetime, Field(serialization_alias="minuteInterval")]

    @field_validator("minute_interval", mode="after")
    @classmethod
    def validate_minute(cls, minute_interval: datetime) -> time:
        return convert_datetime_to_time(minute_interval)


class MaxMemoryPerHour(MemoryBase):
    hour_interval: Annotated[datetime, Field(serialization_alias="hourInterval")]

    @field_validator("hour_interval", mode="after")
    @classmethod
    def validate_minute(cls, hour_interval: datetime) -> time:
        return convert_datetime_to_time(hour_interval)


class CpuBase(BaseModel):
    cpu_usage: Annotated[float, Field(serialization_alias="cpuUsage")]


class MaxCpuPerMinute(CpuBase):
    minute_interval: Annotated[datetime, Field(serialization_alias="minuteInterval")]

    @field_validator("minute_interval", mode="after")
    @classmethod
    def validate_minute(cls, minute_interval: datetime) -> time:
        return convert_datetime_to_time(minute_interval)


class MaxCpuPerHour(CpuBase):
    hour_interval: Annotated[datetime, Field(serialization_alias="hourInterval")]

    @field_validator("hour_interval", mode="after")
    @classmethod
    def validate_minute(cls, hour_interval: datetime) -> time:
        return convert_datetime_to_time(hour_interval)


class DiskBase(BaseModel):
    disk_usage: Annotated[float, Field(serialization_alias="diskUsage")]


class MaxDiskPerMinute(DiskBase):
    minute_interval: Annotated[datetime, Field(serialization_alias="minuteInterval")]

    @field_validator("minute_interval", mode="after")
    @classmethod
    def validate_minute(cls, minute_interval: datetime) -> time:
        return convert_datetime_to_time(minute_interval)


class MaxDiskPerHour(DiskBase):
    hour_interval: Annotated[datetime, Field(serialization_alias="hourInterval")]

    @field_validator("hour_interval", mode="after")
    @classmethod
    def validate_minute(cls, hour_interval: datetime) -> time:
        return convert_datetime_to_time(hour_interval)
