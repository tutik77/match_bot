from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession


import tables
from settings import settings


engine = create_async_engine(
    settings.database_url,
)

Session = sessionmaker(
    class_=AsyncSession,
    bind=engine, 
    autoflush=False,    
    autocommit=False,
    expire_on_commit=False,
)

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(tables.Base.metadata.create_all)

async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session