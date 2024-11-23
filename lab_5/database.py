from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import settings


meta_data = MetaData()

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg(),
    echo=True
)

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg(),
    echo=True
)

class Base(DeclarativeBase):
    pass

sync_session_factory = sessionmaker(sync_engine)
async_session_factory = async_sessionmaker(async_engine)