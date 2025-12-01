from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from contrib.database import engine
from contrib.models import Base

# Importar os roteadores dos nossos módulos
from plano_manutencao import controller as plano_controller
from unidade_operacional import controller as uop_controller
from viatura import controller as viatura_controller

# --- Alembic ---
# Importar os models para que o Alembic possa "vê-los"
from plano_manutencao.models import PlanoDeManutencaoModel
from unidade_operacional.models import UnidadeOperacionalModel
from viatura.models import ViaturaModel

# Metadados das Tags para a documentação
tags_metadata = [
    {
        "name": "Viaturas",
        "description": "Gerenciamento da frota veicular. Permite **cadastro**, **busca** e **listagem** detalhada de viaturas.",
    },
    {
        "name": "Unidades Operacionais",
        "description": "Gestão das UOPs (Delegacias e Postos). Controla onde as viaturas estão alocadas.",
    },
    {
        "name": "Planos de Manutenção",
        "description": "Controle financeiro e técnico dos planos de revisão e manutenção preventiva.",
    },
]

# Criar a instância principal da aplicação FastAPI
app = FastAPI(
    title="🚔 ViaturaAPI - Gestão de Frota PRF",
    version="1.1.0",
    description="Sistema de Gestão Inteligente de Viaturas da PRF",
    openapi_tags=tags_metadata,
)

# Isso libera o acesso para o seu Frontend React
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "*" # Libera geral (apenas para desenvolvimento)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Permite GET, POST, DELETE, etc.
    allow_headers=["*"], # Permite todos os cabeçalhos
)
# ------------------------------------------

# Incluir os roteadores de cada módulo
app.include_router(plano_controller.router)
app.include_router(uop_controller.router)
app.include_router(viatura_controller.router)

# Habilitar a paginação
add_pagination(app)

# Função para criar as tabelas ao iniciar
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)