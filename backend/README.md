# Backend — VIATURA

API de gestão de frota em Python 3.12, FastAPI, SQLAlchemy assíncrono e PostgreSQL.
Parte do [projeto unificado](../README.md); a interface está em [frontend/](../frontend/README.md).

## Executar com Docker

Na **raiz do repositório**, `docker compose up --build -d --wait` inicia o sistema
completo. Veja a configuração e o seed no [guia principal](../README.md).

## Desenvolvimento local

Os comandos abaixo partem de `backend/`. Requisitos: Python 3.12 e PostgreSQL.

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
Copy-Item .env.example .env
```

Em Linux/macOS, use `source .venv/bin/activate` e `cp .env.example .env`.
Configure `DB_URL` no `.env`. Para usar apenas o banco do Docker, execute
`docker compose up -d db` na raiz, com usuário/senha/banco correspondentes.

Em um banco **novo e vazio**, aplique o schema e inicie a API:

```bash
python -m alembic upgrade head
python -m uvicorn main:app --reload --port 8000
```

Swagger: http://localhost:8000/docs. Não execute a migração inicial sobre um
banco já criado pelo seed ou por `create_all` sem reconciliar seu histórico.

## Verificações

Dentro de `backend/`, com o ambiente Python ativo:

```bash
python -m ruff check .
python -m pytest --cov --cov-report=term-missing --cov-fail-under=85
```

A suíte tem 35 testes e usa SQLite em memória, sem exigir um PostgreSQL ativo.
O CI também inicia uma instância PostgreSQL no teste de integração do Compose.

## Endpoints

| Método | Rota | Função |
|---|---|---|
| `POST` | `/viaturas/` | Cadastrar veículo |
| `GET` | `/viaturas/` | Listagem paginada, com filtros por modelo, placa e status |
| `GET` | `/viaturas/previsao-orcamentaria` | Contagem e custo previsto da frota |
| `GET` | `/viaturas/{id}` | Consultar veículo |
| `PATCH` | `/viaturas/{id}/status` | Alterar situação operacional |
| `PATCH` | `/viaturas/{id}/alocacao` | Transferir veículo para outra unidade |
| `GET/POST` | `/uops/` | Consultar/cadastrar unidades |
| `GET/POST` | `/planos/` | Consultar/cadastrar planos |
| `GET` | `/health` | Verificar disponibilidade da aplicação |

![Documentação Swagger.](img/01_swagger.png)

## Organização do código

Cada módulo de negócio contém `models.py` (persistência), `schemas.py` (contrato e
validação) e `controller.py` (rotas e regras). `contrib/` reúne configuração, sessão
de banco e classes base. `main.py` monta a aplicação, CORS e roteadores.

As regras de baixa definitiva e exclusão dos baixados do orçamento têm testes
próprios em [tests/](tests/). A previsão é agregada em SQL para não depender do
tamanho da página exibida no frontend.

## Configuração

| Variável | Uso |
|---|---|
| `DB_URL` | URL SQLAlchemy com driver `asyncpg` |
| `CORS_ORIGINS` | Origens do frontend separadas por vírgula |
| `SQL_ECHO` | Exibição das queries, `false` por padrão |

O arquivo [`.env.example`](.env.example) é para execução local. No Compose, essas
variáveis são injetadas pela configuração da raiz. Mantenha `.env` fora do Git.

`seed.py` contém apenas dados fictícios, mas **apaga e recria as tabelas** antes
de populá-las. Use exclusivamente em banco de demonstração.

A API ainda não possui autenticação/autorização. Planeje essa camada antes de
permitir acesso a dados de uma operação real.
