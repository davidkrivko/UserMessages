from pydantic.v1 import BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel


class Settings(BaseSettings):
    PSQL_DB_URL: str

    class Config:
        env_file = '.env'


settings = Settings()

# Create async engine
engine = create_async_engine(settings.PSQL_DB_URL, echo=True)


async def init_database():
    async with engine.begin() as conn:
        from src.users.models import CustomUsersDB
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncSession:
    async_session = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with async_session() as session:
        yield session
