from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict
import os

class Settings(BaseSettings):
    DB_URL: str = "postgresql+asyncpg://prf_user:prf_pass@127.0.0.1:5432/viatura_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()

engine = create_async_engine(settings.DB_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()