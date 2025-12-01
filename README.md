# 💻 Viatura Frontend: Dashboard de Gestão de Frotas

[![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5-646CFF?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev/)
[![Chakra UI](https://img.shields.io/badge/Chakra%20UI-v3-319795?style=for-the-badge&logo=chakraui&logoColor=white)](https://chakra-ui.com/)

Interface moderna e responsiva para o sistema de gestão de viaturas da PRF. Este projeto consome a **ViaturaAPI** para fornecer visualização de dados em tempo real, controle de custos e monitoramento operacional.

> **Nota:** Este é o FRONTEND (Interface). Para funcionar, ele precisa do [Backend ViaturaAPI](https://github.com/SEU-USUARIO/Viatura_API) rodando localmente.

---

### ✨ Funcionalidades Visuais

* **📊 Dashboard Estratégico:**
    * Cartões de métricas com indicadores de frota ativa, custos e viaturas em manutenção.
    * Feedback visual de carregamento com *Skeletons*.
    * Indicadores coloridos para status do sistema.

* **🚙 Gestão de Viaturas:**
    * Tabela interativa com listagem de veículos.
    * **Barra de Pesquisa Instantânea:** Filtre por placa ou modelo em tempo real.
    * **Badges Inteligentes:** Cores dinâmicas para status (Operação/Manutenção) e ano de fabricação.

* **💰 Visualização Financeira:**
    * Formatação automática de moeda (BRL/R$) para planos de manutenção.
    * Indicadores claros de custos preventivos e corretivos.

---

### 🛠️ Tecnologias Utilizadas

* **Linguagem:** TypeScript (Segurança e tipagem estática).
* **Framework:** React 18 (Componentização).
* **Build Tool:** Vite (Performance extrema no desenvolvimento).
* **UI Kit:** Chakra UI v3 (Componentes acessíveis e tema customizável).
* **HTTP Client:** Axios (Comunicação com a API).
* **Roteamento:** React Router DOM.

---

### 🚀 Como Rodar o Projeto

#### 1. Pré-requisitos
* Node.js 18+ instalado.
* O **Backend** deve estar rodando na porta `8000` (Verifique o repositório da API).

#### 2. Instalação

Clone este repositório e instale as dependências:

```bash
# Clone o projeto
git clone [https://github.com/SEU-USUARIO/Viatura-Frontend.git](https://github.com/SEU-USUARIO/Viatura-Frontend.git)
cd Viatura-Frontend

# Instale os pacotes (NPM)
npm install
```

#### 3. Execução
Inicie o servidor de desenvolvimento:

```
npm run dev
```

O terminal exibirá o link de acesso, geralmente: 👉 http://localhost:5173

### ⚙️ Configuração da API
A conexão com o Backend é gerenciada em src/services/api.ts. Por padrão, ele aponta para o endereço local do FastAPI:

```
baseURL: '[http://127.0.0.1:8000](http://127.0.0.1:8000)'
``` 

Caso precise alterar a porta ou o IP do servidor, modifique este arquivo.

### 📂 Estrutura de Pastas
* src/pages: Telas completas (Dashboard, Viaturas, UOPs, Planos).
* src/components: Blocos reutilizáveis (Navbar, Cards, Tabelas).
* src/services: Configuração do Axios.
* src/types: Definições de Tipos (Interfaces TypeScript para Viatura, UOP, Plano).

### 🤝 Contribuição
Projeto desenvolvido com foco em Clean Code, componentização e usabilidade. Pull Requests são bem-vindos!
