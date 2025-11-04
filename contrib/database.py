from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
import os

# --- URL DE CONEXÃO ATUALIZADA ---
# Formato: postgresql+asyncpg://USUARIO:SENHA@HOST:PORTA/NOME_DO_BANCO
DB_CONNECTION_STRING = "postgresql+asyncpg://prf_user:prf_pass@localhost:5432/viatura_db"


class Settings(BaseSettings):
    # Tenta pegar do ambiente, se não, usa a string que definimos acima
    DB_URL: str = os.getenv("DB_URL", DB_CONNECTION_STRING)

settings = Settings()

# Cria o "motor" de conexão assíncrono
engine = create_async_engine(settings.DB_URL, echo=True)

# Cria a fábrica de sessões (sessionmaker)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Função para ser usada como Dependência (Depends) no FastAPI
async def get_db_session() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()