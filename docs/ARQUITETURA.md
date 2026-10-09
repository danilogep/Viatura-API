# Arquitetura

## Fluxo da aplicação

```text
Navegador
    ├── React / TypeScript, servido por Vite (dev) ou nginx (Docker)
    └── HTTP para FastAPI
                  └── SQLAlchemy assíncrono
                            └── PostgreSQL
```

O navegador acessa a API pela URL de `VITE_API_URL`. O host `api`, usado entre
containers, não é uma URL acessível pelo navegador do usuário. Por isso o Compose
usa `http://localhost:API_PORT` por padrão, e o backend libera a origem do frontend
via CORS.

## Responsabilidades

- `backend/`: validação Pydantic, regras de negócio, persistência, migrações e testes.
- `frontend/`: navegação, telas, estado da interface e consumo dos endpoints.
- `docker-compose.yml`: conecta banco, backend e frontend; não contém regras de negócio.
- `.github/workflows/`: única configuração de CI, com jobs separados por camada.
- `docs/`: decisões que afetam o projeto completo. Detalhes de execução ficam nos READMEs das camadas.

Os módulos Python foram mantidos para evitar misturar a migração de repositórios
com uma refatoração da aplicação. Os comandos Python são executados dentro de
`backend/`; os comandos npm, dentro de `frontend/`.

## Dependências e configuração

As camadas mantêm seus próprios manifestos: `requirements.txt` e
`requirements-dev.txt` para Python; `package.json` e `package-lock.json` para Node.
Não há um ambiente Python ou `node_modules` compartilhado na raiz.

| Arquivo local | Consumidor | Uso |
|---|---|---|
| `.env` na raiz | Docker Compose | Banco, portas, CORS e argumento de build |
| `backend/.env` | Pydantic Settings | Execução Python fora do Docker |
| `frontend/.env` | Vite | Execução/build React fora do Compose |

Todos são ignorados pelo Git. Somente os arquivos `.env.example` são publicados.
O Compose injeta as variáveis do backend diretamente no container; ele não exige
um `backend/.env`. Variáveis `VITE_*` são públicas no bundle do navegador e nunca
devem conter segredos.

## Banco e migrações

O Compose usa um volume nomeado `pg_data`. O nome do projeto permanece
`viatura_api`, compatível com o diretório anterior, para evitar trocar
silenciosamente a associação com o volume. `-p` permite ambientes independentes.

A API mantém a criação de tabelas com `create_all` na inicialização para facilitar
a demonstração. O histórico de mudanças do schema está em `backend/alembic/`.
Para uma base versionada, aplique as migrações antes de iniciar a API; não confunda
criação automática de tabelas com aplicação de migrações. Não aplique a migração
inicial cegamente sobre uma base já criada por `create_all` ou pelo seed.

O `seed.py` é destrutivo para as tabelas da aplicação e serve exclusivamente
para uma base de demonstração.

## Validação

1. Backend: lint e testes com cobertura mínima de 85%, em SQLite em memória.
2. Frontend: lint, TypeScript e bundle de produção.
3. Integração: construir ambas as imagens, iniciar PostgreSQL/API/nginx e verificar
   health, listagem da frota e fallback de rota do React.

O teste de integração não substitui testes de navegador nem de concorrência em
PostgreSQL. Não há autenticação na API nesta versão.
