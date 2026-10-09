# Migração para o repositório unificado

## Estrutura anterior e atual

| Antes | Agora |
|---|---|
| Pasta `Viatura_API/` com os módulos Python na raiz | `Viatura/backend/` |
| Pasta independente `viatura-frontend/` | `Viatura/frontend/` |
| Dois clones para executar o Compose | Um clone de `danilogep/Viatura-API` |
| Workflow em cada repositório | CI único na raiz, com jobs por camada |
| `FRONTEND_PATH` apontando para outra pasta | Contexto fixo `./frontend` |

O endereço principal continua sendo
https://github.com/danilogep/Viatura-API. O nome preserva links existentes;
o conteúdo agora representa o sistema completo.

## Histórico

O backend foi movido em um commit próprio. O frontend foi integrado com
`git subtree add --prefix=frontend`, **sem `--squash`**. Os commits originais
continuam acessíveis no histórico do repositório unificado.

Para consultar o histórico anterior do frontend, use `git log --all --graph`.
Os commits antigos conservam os caminhos que existiam no repositório original;
filtrar apenas por `frontend/` não mostra necessariamente esses commits anteriores
ao merge. Para o backend, `git log --follow -- backend/main.py` acompanha a mudança
de caminho.

## Desenvolvimento local

1. Abra a pasta `Viatura` inteira no editor.
2. Selecione um interpretador Python dentro de `backend/.venv`.
3. Recrie ambientes virtuais antigos após mover as pastas: scripts de ativação e
   executáveis podem conter caminhos absolutos. As dependências estão nos manifests.
4. Execute `npm ci` em `frontend/` em uma instalação nova.
5. Use `.env` da raiz para Docker; use os exemplos de cada camada para execução local.

O banco de desenvolvimento local pertence ao backend. Não versione `.env`,
arquivos `.db`, caches ou dependências instaladas.

## Docker e dados existentes

O Compose mantém o nome `viatura_api` e o volume lógico `pg_data`. Se o ambiente
anterior foi iniciado com `docker compose -p nome-personalizado`, continue usando
o mesmo `-p` ou `COMPOSE_PROJECT_NAME` para acessar seu volume.

Contêineres antigos precisam estar encerrados antes de usar as mesmas portas.
Não use `down --volumes` para migrar um banco que deseja preservar. O seed também
apaga dados; não faz parte da migração.

Para conferir somente a configuração, sem subir serviços:

```bash
docker compose config --quiet
```

Atualize atalhos, configurações do editor e serviços externos que ainda apontem
para a raiz Python antiga ou para o clone independente do frontend. Builds avulsos
agora usam `docker build ./backend` ou `docker build ./frontend`.
