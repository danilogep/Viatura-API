from collections.abc import AsyncGenerator

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine


class Settings(BaseSettings):
    """Configuração da aplicação, lida de variáveis de ambiente ou do arquivo .env."""

    # Credencial de desenvolvimento; em qualquer outro ambiente vem do ambiente.
    DB_URL: str = "postgresql+asyncpg://viatura:viatura@127.0.0.1:5432/viatura_db"

    # Origens liberadas no CORS, separadas por vírgula.
    CORS_ORIGINS: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Ecoa o SQL gerado no console. Desligado por padrão: com echo ligado,
    # qualquer log de produção vaza o conteúdo das queries.
    SQL_ECHO: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]


settings = Settings()

engine = create_async_engine(settings.DB_URL, echo=settings.SQL_ECHO)
async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
