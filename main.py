from fastapi import FastAPI
from fastapi_pagination import add_pagination # <-- DESAFIO 4: Importar
from contrib.database import engine
from contrib.models import Base     

# Importar os roteadores dos nossos módulos
from plano_manutencao import controller as plano_controller
from unidade_operacional import controller as uop_controller
from viatura import controller as viatura_controller

# --- Alembic ---
# Importar os models para que o Alembic possa "vê-los"
# Embora não pareçam ser usados diretamente aqui,
# eles precisam ser importados em algum lugar que o __init__.py principal veja,
# para que o Alembic detecte as tabelas.
from plano_manutencao.models import PlanoDeManutencaoModel
from unidade_operacional.models import UnidadeOperacionalModel
from viatura.models import ViaturaModel
# ---------------

# Criar a instância principal da aplicação FastAPI
app = FastAPI(
    title="ViaturaAPI",
    version="1.0.0",
    description="API para gestão de viaturas e planos de manutenção da PRF"
)

# Incluir os roteadores de cada módulo
app.include_router(plano_controller.router)
app.include_router(uop_controller.router)
app.include_router(viatura_controller.router)

# --- DESAFIO 4 (Finalização): Habilitar a paginação ---
# Esta linha "ativa" a paginação em toda a aplicação
add_pagination(app)

# (Opcional) Função para criar as tabelas ao iniciar (bom para testes)
# Em produção, usamos Alembic (migrations)
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Cuidado: apaga tudo
        await conn.run_sync(Base.metadata.create_all)