# 🚀 ViaturaAPI: Gerenciamento de Viaturas da PRF

[![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com)

Bem-vindo à **ViaturaAPI**, uma API RESTful desenvolvida em Python com FastAPI, projetada para gerenciar eficientemente as viaturas da Polícia Rodoviária Federal (PRF), seus planos de manutenção e as unidades operacionais.

Este projeto foi construído para demonstrar conceitos modernos de desenvolvimento de APIs, incluindo integração com banco de dados PostgreSQL, gerenciamento de migrações com Alembic, paginação de resultados e tratamento de erros customizado.

> **Nota:** Este repositório contém o BACKEND (API). Para ver a interface visual, acesse o repositório do Frontend.

---

### 🌟 Novas Funcionalidades (v2.0)

* **💰 Inteligência Financeira:**
    * Cálculo automático de previsão orçamentária baseado nos planos de manutenção ativos.
    * Registro de valores estimados para serviços preventivos e corretivos.

* **🚦 Controle de Status Operacional:**
    * Monitoramento em tempo real: Saiba quantas viaturas estão **"Em Operação"** vs **"Em Manutenção"**.
    * Lógica de negócios para impedir alocação de viaturas baixadas.

* **🔍 Filtros Avançados:**
    * Busca otimizada por Placa, Modelo e Status.
    * Paginação eficiente para grandes volumes de dados.

* **🛡️ Segurança e Robustez:**
    * Tratamento de erros de banco de dados (Integrity Error).
    * Prevenção contra Race Conditions (Condição de Corrida) no cadastro.
    * Configuração segura de CORS para integração com Frontend moderno.

---

### 💻 Tecnologias Utilizadas

* **Linguagem:** Python 3.12+
* **Framework:** FastAPI (Alta performance e validação automática).
* **Banco de Dados:** PostgreSQL (via Docker).
* **ORM:** SQLAlchemy 2.0 (Gerenciamento de dados assíncrono).
* **Migrações:** Alembic (Controle de versão do banco de dados).
* **Ambiente:** Docker & Docker Compose.
* **Validação:** Pydantic (Segurança e tipagem de dados).
---

### 🚀 Primeiros Passos

Siga estas instruções para configurar e executar a ViaturaAPI em seu ambiente local.

#### 1. Pré-requisitos

Certifique-se de ter os seguintes programas instalados em sua máquina:

* **Python 3.12+**: [Download Python](https://www.python.org/downloads/)
* **Docker Desktop**: [Download Docker](https://www.docker.com/products/docker-desktop/) (Inclui Docker Compose)
* **Git**: [Download Git](https://git-scm.com/downloads)

#### 2. Clone o Repositório

Abra seu terminal (PowerShell no Windows, Terminal no Linux/macOS) e clone este repositório:

```bash
git clone [https://github.com/seu-usuario/Viatura_API.git](https://github.com/seu-usuario/Viatura_API.git)
cd Viatura_API
```

#### 3. Configuração do Ambiente

##### a. Ambiente Virtual

Crie e ative um ambiente virtual para o projeto:

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# Ativar o ambiente virtual (Linux/macOS)
# source venv/bin/activate
```

##### b. Instale as Dependências

Com o ambiente virtual ativado, instale todas as bibliotecas necessárias:

```bash
pip install -r requirements.txt
```

#### 4. Inicie o Banco de Dados (PostgreSQL com Docker)

Nós usamos Docker para manter o banco de dados isolado e fácil de configurar.

```bash
docker compose up -d

# 2. Criar tabelas e popular dados (Seed)
python seed.py
```

Este comando irá baixar a imagem do PostgreSQL (se ainda não tiver) e iniciar o container do banco de dados em segundo plano.

#### 5. Execute as Migrações do Banco de Dados

Com o banco de dados rodando, use o Alembic para criar as tabelas no PostgreSQL:

```bash
alembic upgrade head
```

Você verá mensagens informando que as tabelas `plano_de_manutencaos`, `unidade_operacionals` e `viaturas` foram criadas.

---

### 🌐 Utilizando a API

Com todas as configurações feitas, é hora de rodar a API e começar a interagir com ela!

#### 1. Inicie o Servidor da API

No seu terminal (com o ambiente virtual ainda ativado), inicie o servidor FastAPI:

```bash
uvicorn main:app --reload --port 8000
```

Você verá uma mensagem indicando que o Uvicorn está rodando em `http://127.0.0.1:8000`.

#### 2. Acesse a Documentação Interativa (Swagger UI)

Abra seu navegador e acesse a documentação interativa da API:

➡️ **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

Você também pode acessar a documentação ReDoc em [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc).

Aqui você encontrará todos os *endpoints* disponíveis, exemplos de requisições e poderá testar a API diretamente pelo navegador.

---

### 🛑 Parando o Ambiente

Para parar o servidor FastAPI, pressione `CTRL + C` no terminal onde ele está rodando.

Para parar e remover os containers do Docker (e opcionalmente os dados do banco de dados), use:

```bash
# Para parar os containers
docker compose stop

# Para parar e remover os containers e a rede (mantém os dados)
docker compose down

# Para parar e remover TUDO (containers, rede, e VOLUMES com os dados do banco!)
docker compose down -v
```

---

### 🤝 Integração Frontend
Este backend foi desenhado para alimentar o *Viatura Frontend*, desenvolvido em React + TypeScript. Certifique-se de que este backend esteja rodando na porta 8000 para que o frontend funcione corretamente.

---

### 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests*.