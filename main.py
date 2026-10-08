from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from contrib.database import engine, settings
from contrib.models import Base

# Importar os roteadores dos nossos módulos
from plano_manutencao import controller as plano_controller

# Importar os models para que o Alembic e o create_all possam "vê-los"
from plano_manutencao.models import PlanoDeManutencaoModel  # noqa: F401
from unidade_operacional import controller as uop_controller
from unidade_operacional.models import UnidadeOperacionalModel  # noqa: F401
from viatura import controller as viatura_controller
from viatura.models import ViaturaModel  # noqa: F401

tags_metadata = [
    {
        "name": "Viaturas",
        "description": (
            "Gerenciamento da frota. Permite **cadastro**, **busca**, **listagem paginada**, "
            "mudança de situação operacional e **previsão orçamentária** do ciclo de manutenção."
        ),
    },
    {
        "name": "Unidades Operacionais",
        "description": "Gestão das unidades que respondem pelos veículos.",
    },
    {
        "name": "Planos de Manutenção",
        "description": "Controle financeiro e técnico dos planos de revisão e manutenção preventiva.",
    },
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Conveniência de desenvolvimento: em ambiente versionado o schema é criado
    # pelo Alembic (`alembic upgrade head`), não aqui.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="ViaturaAPI — Gestão de Frota Operacional",
    version="2.0.0",
    description=(
        "API de gestão de frota de veículos operacionais: cadastro, alocação por "
        "unidade, controle de situação e previsão de custo de manutenção."
    ),
    openapi_tags=tags_metadata,
    lifespan=lifespan,
)

# Origens explícitas: com allow_credentials=True o navegador recusa "*",
# então a lista vem de CORS_ORIGINS e tem um valor local por padrão.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plano_controller.router)
app.include_router(uop_controller.router)
app.include_router(viatura_controller.router)


@app.get("/health", tags=["Infraestrutura"], summary="Verificação de disponibilidade")
async def health() -> dict[str, str]:
    """Usado pelo healthcheck do docker-compose para liberar o start do frontend."""
    return {"status": "ok"}


add_pagination(app)
