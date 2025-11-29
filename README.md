# 🚀 ViaturaAPI: Gerenciamento de Viaturas da PRF

Bem-vindo à **ViaturaAPI**, uma API RESTful desenvolvida em Python com FastAPI, projetada para gerenciar eficientemente as viaturas da Polícia Rodoviária Federal (PRF), seus planos de manutenção e as unidades operacionais.

Este projeto foi construído para demonstrar conceitos modernos de desenvolvimento de APIs, incluindo integração com banco de dados PostgreSQL, gerenciamento de migrações com Alembic, paginação de resultados e tratamento de erros customizado.

---

### 🌟 Funcionalidades Principais

* **🚗 Gestão Completa de Viaturas:**
    * Cadastro detalhado com **Placa, Marca, Modelo, Cor e Ano**.
    * Sistema inteligente que impede duplicidade de placas.
    * Busca avançada e filtros dinâmicos.

* **💰 Controle Financeiro de Manutenção:**
    * Cadastro de Planos de Manutenção (ex: "Revisão de Freios").
    * **Novidade:** Registro de custos estimados para cálculos orçamentários futuros.

* **🏢 Logística Operacional (UOPs):**
    * Gestão de Unidades Operacionais.
    * Controle de alocação: saiba exatamente onde cada viatura está lotada.

* **🛡️ Segurança e Performance:**
    * Proteção contra credenciais expostas (Environment Variables).
    * Tratamento robusto de erros de banco de dados (Integrity Errors).
    * Paginação automática para lidar com grandes volumes de dados.

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

### 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir *issues* ou enviar *pull requests*.