from sqlalchemy import MetaData, INTEGER, FLOAT
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.config import settings
from src.constants import DB_NAMING_CONVENTION
from src.metrics import types


class Base(DeclarativeBase, MappedAsDataclass):
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
    type_annotation_map = {
        types.MetricId: INTEGER,
        types.MemoryUsage: FLOAT,
        types.CpuUsage: FLOAT,
        types.DiskSpaceTotal: INTEGER,
        types.DiskSpaceUsed: INTEGER,
        types.DiskUsage: FLOAT
    }


async_engine: AsyncEngine = create_async_engine(str(settings.POSTGRES_URL))

async def db_session() -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(async_engine, expire_on_commit=False)
