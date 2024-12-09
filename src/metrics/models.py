import sqlalchemy as sa
import sqlalchemy.orm as so
from datetime import datetime

from src.database import Base
from src.metrics import types


class Metric(Base):
    __tablename__ = "metrics"

    id: so.Mapped[types.MetricId] = so.mapped_column(
        primary_key=True, autoincrement=True
    )
    memory_usage: so.Mapped[types.MemoryUsage]
    cpu_usage: so.Mapped[types.CpuUsage]
    disk_spaca_total: so.Mapped[types.DiskSpaceTotal]
    disk_space_used: so.Mapped[types.DiskSpaceUsed]
    disk_usage: so.Mapped[types.DiskUsage]
    created_at: so.Mapped[datetime] = so.mapped_column(
        sa.TIMESTAMP(timezone=True), server_default=sa.func.now()
    )
