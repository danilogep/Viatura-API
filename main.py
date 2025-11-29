from fastapi import FastAPI
from fastapi_pagination import add_pagination
from contrib.database import engine
from contrib.models import Base

# Importar os roteadores dos nossos módulos
from plano_manutencao import controller as plano_controller
from unidade_operacional import controller as uop_controller
from viatura import controller as viatura_controller

# --- Alembic ---
from plano_manutencao.models import PlanoDeManutencaoModel
from unidade_operacional.models import UnidadeOperacionalModel
from viatura.models import ViaturaModel
# ---------------

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

# Criar a instância principal da aplicação FastAPI com DESIGN PREMUIM
app = FastAPI(
    title="🚔 ViaturaAPI - Gestão de Frota PRF",
    version="1.1.0",
    description="""
    ## 🚀 Sistema de Gestão Inteligente de Viaturas
    
    Esta API fornece serviços completos para o controle de frota da Polícia Rodoviária Federal.
    
    ### Funcionalidades Principais:
    * **Controle de Viaturas**: Rastreamento de marca, modelo, cor e placa.
    * **Gestão Financeira**: Cálculo automático de custos de manutenção.
    * **Alocação**: Distribuição de viaturas por Unidades Operacionais (UOPs).
    
    ---
    *Desenvolvido para fins didáticos.*
    """,
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Suporte Técnico ViaturaAPI",
        "url": "http://meu-portfolio.com/contact",
        "email": "suporte@viaturaapi.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=tags_metadata, # Aplica as descrições das tags definidas acima
)

# Incluir os roteadores de cada módulo
app.include_router(plano_controller.router)
app.include_router(uop_controller.router)
app.include_router(viatura_controller.router)

# Habilitar a paginação
add_pagination(app)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)