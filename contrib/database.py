from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings, SettingsConfigDict # Importando ConfigDict para configurações extras
import os

class Settings(BaseSettings):
    # Configuração do Pydantic para ler variáveis de ambiente
    # Caso não encontre no sistema, usa o valor padrão definido abaixo.
    # OBS: Em produção, JAMAIS deixe senhas padrão aqui. Passe via .env ou variáveis de sistema.
    DB_URL: str = "postgresql+asyncpg://prf_user:prf_pass@localhost:5432/viatura_db"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

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