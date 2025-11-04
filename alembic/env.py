import sys
import os
from logging.config import fileConfig
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
import asyncio

# Adiciona o diretório raiz do projeto ao sys.path
# Isso permite que o Alembic encontre 'contrib', 'viatura', etc.
# __file__ se refere a este arquivo (env.py)
# os.path.dirname(__file__) se refere à pasta (alembic/)
# os.path.join(..., '..') volta um nível (para a raiz Viatura_API/)
# os.path.abspath garante que seja um caminho absoluto
project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_dir)


# --- NOSSA CONFIGURAÇÃO ---
# Importar a URL do banco e a Base dos nossos models
from contrib.database import settings  # Importa nossas configurações (que têm o DB_URL)
from contrib.models import Base        # Importa nossa Base(Model)

# Importar todos os models para que o Alembic "veja" eles
import plano_manutencao.models
import unidade_operacional.models
import viatura.models
# -------------------------

# Esta é a configuração do Alembic
config = context.config

# Interpretar o arquivo .ini
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# --- NOSSA CONFIGURAÇÃO ---
# Definir o 'target_metadata' para a nossa Base(Model)
# Isso diz ao Alembic quais tabelas ele deve monitorar
target_metadata = Base.metadata

# Definir a URL do banco de dados
# (Substituímos o 'sqlalchemy.url' do .ini por esta)
# Usamos a DB_URL síncrona, trocando o driver asyncpg por psycopg2
# pois o Alembic não suporta async na conexão principal
sync_db_url = settings.DB_URL.replace("postgresql+asyncpg", "postgresql+psycopg2")
config.set_main_option("sqlalchemy.url", sync_db_url)
# -------------------------


def do_run_migrations(connection):
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        render_as_batch=True # Adicionado para compatibilidade com SQLite se necessário
    )

    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Executa as migrations no modo 'online' (conectado ao banco)."""
    
    # Usar o create_async_engine do nosso database.py (com driver async)
    connectable = create_async_engine(settings.DB_URL)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()

if context.is_offline_mode():
    # run_migrations_offline() # Não vamos suportar modo offline por simplicidade
    raise NotImplementedError("Modo offline não suportado.")
else:
    # O Alembic não roda bem com asyncio.run() diretamente aqui
    # Vamos usar a engine síncrona que definimos no config
    
    # Criar engine síncrona para o Alembic
    from sqlalchemy import create_engine
    engine = create_engine(config.get_main_option("sqlalchemy.url"))
    
    with engine.connect() as connection:
        do_run_migrations(connection)