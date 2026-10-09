# VIATURA — gestão de frota operacional

[![CI](https://github.com/danilogep/Viatura-API/actions/workflows/ci.yml/badge.svg)](https://github.com/danilogep/Viatura-API/actions/workflows/ci.yml)
[![Licença MIT](https://img.shields.io/badge/licença-MIT-green)](LICENSE)

Sistema full stack para cadastrar veículos, organizar sua alocação por unidade,
acompanhar a situação operacional e projetar o custo dos planos de manutenção.
**FastAPI, SQLAlchemy, PostgreSQL, React 19 e TypeScript**, em um único repositório.

![Painel com frota ativa, previsão de gastos e veículos em manutenção.](frontend/img/01_dashboard.png)

## Onde encontrar cada parte

```text
Viatura/
├── backend/                 API Python, banco, migrações e testes
│   ├── main.py              Entrada do FastAPI
│   ├── contrib/             Configuração, sessão e modelos base
│   ├── viatura/             Veículos e regras da frota
│   ├── unidade_operacional/ Unidades responsáveis pelos veículos
│   ├── plano_manutencao/    Planos e custos estimados
│   ├── alembic/             Migrações do banco
│   ├── tests/               Testes automatizados
│   ├── requirements*.txt    Dependências Python
│   └── Dockerfile
├── frontend/                Aplicação React + TypeScript
│   ├── src/pages/           Dashboard, veículos, unidades e planos
│   ├── src/components/      Componentes compartilhados
│   ├── src/services/        Cliente HTTP da API
│   ├── src/types/           Tipos e contratos
│   ├── package.json         Dependências e comandos npm
│   └── Dockerfile           Build Vite e entrega via nginx
├── docs/                    Arquitetura e guia de migração
├── .github/workflows/ci.yml CI das duas camadas e integração Docker
├── .env.example             Configuração do Docker Compose
├── docker-compose.yml       Banco + API + interface
└── LICENSE
```

Comece pelo [backend](backend/README.md) para trabalhar na API ou pelo
[frontend](frontend/README.md) para trabalhar nas telas.
As decisões de organização estão em [Arquitetura](docs/ARQUITETURA.md).

## Rodar o sistema completo

Requisito: Docker com o plugin Docker Compose.
Execute os comandos a partir da raiz do repositório:

```bash
git clone https://github.com/danilogep/Viatura-API.git Viatura
cd Viatura
cp .env.example .env
docker compose up --build -d --wait
```

No PowerShell, `Copy-Item .env.example .env` também faz a cópia.
Configure a senha do banco no `.env` antes da primeira inicialização.

| Serviço | Endereço padrão |
|---|---|
| Interface | http://localhost:5173 |
| Swagger da API | http://localhost:8000/docs |
| Healthcheck | http://localhost:8000/health |
| PostgreSQL | localhost:5432 |

Para mudar as portas, edite `API_PORT`, `FRONTEND_PORT` e `POSTGRES_PORT` no `.env`.
O Compose calcula a URL local da API e as origens CORS a partir dessas portas.
Se definir `VITE_API_URL` ou `CORS_ORIGINS` explicitamente, mantenha-os coerentes
com o endereço de acesso. A URL usada pelo React entra durante o build:

```bash
docker compose up -d --build
```

O banco novo começa vazio. Para carregar dados fictícios de demonstração:

```bash
docker compose --profile seed run --rm seed
```

**O seed apaga e recria as tabelas da aplicação. Use apenas em banco de demonstração.**
Ele gera 5 unidades, 4 planos e 50 veículos, com estados sorteados.

Para acompanhar e encerrar:

```bash
docker compose logs -f api frontend
docker compose down
```

`down` preserva o volume do banco. `down --volumes` apaga os dados desse ambiente.

## Regras de negócio

- **Baixa é definitiva:** veículos baixados não podem retornar à operação ou ser realocados.
- **Orçamento calculado na API:** a soma considera toda a frota elegível, independentemente da paginação da interface.
- **Manutenção continua no orçamento:** veículos baixados são excluídos da previsão.
- **Placa única e relações válidas:** a API valida unidade e plano e trata conflitos de cadastro.

Os testes de [baixa](backend/tests/test_regra_viatura_baixada.py) e
[previsão orçamentária](backend/tests/test_previsao_orcamentaria.py) documentam esses casos.

## Desenvolvimento e validação

| Camada | Guia | Verificações |
|---|---|---|
| Backend | [Setup Python e banco](backend/README.md) | Ruff, pytest e cobertura mínima de 85% |
| Frontend | [Setup Node e API](frontend/README.md) | ESLint, TypeScript e build Vite |
| Integração | [Docker Compose](docker-compose.yml) | Build das imagens, API com PostgreSQL e rotas da SPA |

O [CI](.github/workflows/ci.yml) executa as três verificações a cada push na `main`
e em pull requests. Os testes Python usam SQLite em memória; o teste de integração
do Compose verifica também a inicialização com PostgreSQL.

## Repositório unificado

Este é o repositório principal de **backend e frontend**. Os históricos Git dos
dois projetos foram preservados, sem squash. Quem usava as pastas separadas pode
seguir o [guia de migração](docs/MIGRACAO.md).

## Escopo atual

A API ainda não implementa autenticação e autorização. A configuração apresentada
é de desenvolvimento/demonstração; use dados fictícios. O painel e a API fazem
parte de um projeto de portfólio, com regras e limites documentados.

## Licença e autor

[MIT](LICENSE). Desenvolvido por [Danilo Evangelista](https://github.com/danilogep).
