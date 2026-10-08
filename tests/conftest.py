"""Infraestrutura dos testes.

Cada teste roda contra um SQLite em memória criado do zero, com o `get_db_session`
da aplicação sobrescrito. A escolha é deliberada: a suíte precisa rodar no CI e na
máquina de quem clonou o repositório sem subir um Postgres antes. Os modelos usam
apenas tipos portáveis (String, Integer, Float), então o schema é o mesmo dos dois
lados; o que depende de Postgres — a constraint de unicidade disputada por duas
requisições simultâneas — é exercitado pelo mesmo caminho de erro no SQLite.
"""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from contrib.database import get_db_session
from contrib.models import Base
from main import app

# Importados pelo efeito colateral de registrar as tabelas no metadata.
from plano_manutencao.models import PlanoDeManutencaoModel  # noqa: F401
from unidade_operacional.models import UnidadeOperacionalModel  # noqa: F401
from viatura.models import ViaturaModel  # noqa: F401


@pytest.fixture
async def engine():
    # StaticPool mantém a mesma conexão para todo o teste; sem isso cada conexão
    # nova abriria um banco em memória vazio e diferente.
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest.fixture
async def client(engine):
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async def _get_db_session():
        async with session_factory() as session:
            yield session

    app.dependency_overrides[get_db_session] = _get_db_session

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()


@pytest.fixture
async def uop(client):
    """Uma unidade operacional persistida, pronta para receber viaturas."""
    response = await client.post(
        "/uops/", json={"nome": "UOP 01 - Sede", "municipio": "João Pessoa"}
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
async def uop_secundaria(client):
    response = await client.post(
        "/uops/", json={"nome": "UOP 02 - Litoral", "municipio": "Mamanguape"}
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
async def plano(client):
    """Plano de manutenção de R$ 1.000,00 — valor redondo facilita conferir somas."""
    response = await client.post(
        "/planos/",
        json={
            "nome": "Preventiva Básica (10k)",
            "descricao": "Troca de óleo e filtros.",
            "valor_estimado": 1000.00,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()


@pytest.fixture
def payload_viatura(uop, plano):
    """Fábrica de payloads válidos de viatura, já apontando para a UOP e o plano."""

    def _payload(placa: str = "ABC1D23", **overrides):
        base = {
            "placa": placa,
            "marca": "Chevrolet",
            "modelo": "Trailblazer",
            "cor": "Branca",
            "ano_fabricacao": 2021,
            "unidade_operacional_id": uop["id"],
            "plano_manutencao_id": plano["id"],
        }
        base.update(overrides)
        return base

    return _payload


@pytest.fixture
async def viatura(client, payload_viatura):
    response = await client.post("/viaturas/", json=payload_viatura())
    assert response.status_code == 201, response.text
    return response.json()
