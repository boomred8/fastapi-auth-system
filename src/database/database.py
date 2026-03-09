from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from fastapi import Depends
from typing import Annotated

from src.take_env import database_url

engine = create_async_engine(database_url, echo=True)
async_session = async_sessionmaker(engine,
                                   expire_on_commit=False,
                                   class_=AsyncSession)

async def get_db():
    async with async_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]

