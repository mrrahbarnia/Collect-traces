from sqlalchemy import MetaData, INTEGER, FLOAT, BIGINT
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
    """
    Base class for assigning metadata to tables
    and inheriting from it while creating tables.
    """
    metadata = MetaData(naming_convention=DB_NAMING_CONVENTION)
    type_annotation_map = {
        types.MetricId: INTEGER,
        types.MemoryUsage: FLOAT,
        types.CpuUsage: FLOAT,
        types.DiskSpaceTotal: BIGINT,
        types.DiskSpaceUsed: BIGINT,
        types.DiskUsage: FLOAT
    }

async_engine: AsyncEngine = create_async_engine(str(settings.POSTGRES_URL))

async def db_session() -> async_sessionmaker[AsyncSession]:
    """
    The point of returning async_sessionmaker instead AsyncSession
    is that the openning connecting in pg is costly,
    and if we wanted to open a connection here and pass it as a dependecy,
    we had to keep the connection open in all operations each time.
    but this way i can open connections whenever i want in context_manager and
    close it immediately after that.
    for example:
    
    async def sample_service(db_session: async_sessionmaker[AsyncSession]) -> None:
        async with db_session.begin() as conn:
            SOME OPERATION HERE
        
        async with db_session.begin() as conn:
            SOME OTHER HERE
    """
    return async_sessionmaker(async_engine, expire_on_commit=False)
