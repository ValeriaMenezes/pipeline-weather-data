# Pipeline Weather Data

Projeto de extração de dados de clima via API (OpenWeatherMap), transforma e carrega em um banco PostgreSQL. O projeto inclui uma DAG do Airflow (via `docker-compose`) e módulos Python para executar as fases ETL localmente.

### 🎥 Assista no YouTube
> 🔴 **[Assistir Tutorial Completo](https://www.youtube.com/@vbluuiza)**

---

## 🏗️ Arquitetura do Pipeline

<img src='./img/arquitetura_de_dados_draw.png' alt='Arquitetura do Pipeline ETL'>

---

## 🛠️ Stack Tecnológica

### Core
- **Python 3.14+** - Linguagem principal
- **Apache Airflow 3.1.7** - Orquestração do pipeline
- **PostgreSQL 14** - Banco de dados relacional
- **Docker & Docker Compose** - Containerização

### Bibliotecas Python
- **pandas** - Manipulação e transformação de dados
- **requests** - Requisições HTTP para a API
- **SQLAlchemy** - ORM para interação com o banco de dados
- **psycopg2** - Driver PostgreSQL
- **python-dotenv** - Gerenciamento de variáveis de ambiente

### Outras Ferramentas
- **Redis** - Message broker para Celery
- **Jupyter Notebook** - Análise exploratória de dados
- **UV** - Gerenciador de pacotes Python rápido

**Sumário**
- **Descrição:** ETL de dados meteorológicos para a cidade de São Paulo.
- **Modo de execução:** local (Python) ou via Docker Compose (Airflow).
- **Arquivos principais:** `main.py`, `dags/weather_dag.py`, pasta `src/` (ETL), `config/.env` (variáveis de ambiente).


**Pré-requisitos**

Antes de começar, certifique-se de ter instalado em sua máquina (preferencialmente no ambiente WSL/Linux):
- Git
- Python >= 3.12
- **WSL 2** instalado e rodando no Windows.
- **Docker Desktop** instalado no Windows com a opção **"Use WSL 2 based engine"** ativada nas configurações (o Docker Desktop precisa estar aberto no Windows).
- **uv** instalado no seu terminal WSL (`curl -LsSf https://astral.sh/uv/install.sh | sh`).
- PostgreSQL rodando (localmente ou via Docker)



## 🚀 Instalação e Configuração do Ambiente

1. **Clone o repositório e acesse a pasta do projeto:**

```bash
git clone https://github.com/ValeriaMenezes/pipeline-weather-data/tree/main
cd pipeline_weather_data
```


2. **Criar e ativar um ambiente virtual:**
Como o projeto utiliza o uv e possui um `pyproject.toml`, basta rodar o comando abaixo. Ele criará a pasta .venv automaticamente e instalará todos os pacotes:

```bash
uv sync
```

3. **Ative o ambiente virtual:**

```bash
source .venv/bin/activate
```

4. **Configuração das Variáveis de Ambiente:**
O projeto utiliza a biblioteca python-dotenv para proteger credenciais.
Crie um arquivo `.env` dentro da pasta `config/`:

```bash
API_KEY=sua_api_key_aqui
databse=seu_database_aqui
user=seu_user_aqui
password=sua_senha_aqui
```

**Como Executar a Infraestrutura (Docker, Airflow e PostgreSQL)**

5. O repositório contém um `docker-compose.yaml` configurado para um ambiente Airflow (inclui Postgres e Redis). Use este modo se quiser orquestrar a DAG `weather_pipeline` no Airflow.

6. Inicie o Docker Desktop:
Certifique-se de que o aplicativo do Docker Desktop está aberto e rodando no seu Windows.
No terminal do WSL, dentro da pasta do projeto, execute o comando abaixo para baixar as imagens e iniciar o PostgreSQL e o Airflow em segundo plano:

```bash
docker compose up --build -d
```

7. **Acessar o terminal do PostgreSQL:**
Para criar e acessar o seu banco de dados via WSL, usaremos o psql, que é o terminal interativo do PostgreSQL.

```bash
sudo -u postgres psql
```

No prompt do banco (postgres=#), digite o comando SQL abaixo:

Criar usuário e a senha:

```sql
CREATE USER 'seu_user_aqui' WITH PASSWORD 'sua_senha_aqui';
```

Atribuir poderes de super usuário:

```sql
ALTER USER 'seu_user_aqui' WITH SUPERUSER;
```

Criar o database vinculado ao usuário:

```sql
CREATE DATABASE weather_db owner 'seu_user_aqui;
```

Conecte-se ao novo banco para verificar se deu certo:

```sql
\c weather_db
```

Para sair do terminal do banco e voltar ao WSL, digite `\q` e aperte Enter.

8. **Acesse o Apache Airflow:**
Com os contêineres rodando, abra o seu navegador e acesse a interface do Airflow:

URL: http://localhost:8080

Usuário padrão: airflow
Senha padrão: airflow

9. **Execute a DAG:**
A DAG principal está em `dags/weather_dag.py` com id `weather_pipeline`.


**Executar a pipeline localmente (modo rápido)**

O projeto inclui um script de execução `main.py` que executa as três fases (extract → transform → load). Antes de rodar, verifique `config/.env`.

```bash
uv run main.py
```

10. **Encerrando o Ambiente:**
Quando terminar de trabalhar, pare os contêineres para não consumir memória do seu computador:

```bash
docker compose down
```