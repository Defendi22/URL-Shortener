# URL.SHORT ⚡

> Encurtador de URLs minimalista construído com FastAPI, PostgreSQL, Docker e deploy automático no Render.

![Python](https://img.shields.io/badge/Python-3.11-c8f135?style=flat-square&logo=python&logoColor=white&labelColor=0a0a0a)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-c8f135?style=flat-square&logo=fastapi&logoColor=white&labelColor=0a0a0a)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-c8f135?style=flat-square&logo=postgresql&logoColor=white&labelColor=0a0a0a)
![Docker](https://img.shields.io/badge/Docker-ready-c8f135?style=flat-square&logo=docker&logoColor=white&labelColor=0a0a0a)
![CI](https://img.shields.io/badge/CI-GitHub_Actions-c8f135?style=flat-square&logo=githubactions&logoColor=white&labelColor=0a0a0a)
![Deploy](https://img.shields.io/badge/Deploy-Render-c8f135?style=flat-square&logo=render&logoColor=white&labelColor=0a0a0a)

---

## Sumário

- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Stack](#stack)
- [Arquitetura](#arquitetura)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Como Rodar Localmente](#como-rodar-localmente)
- [Endpoints da API](#endpoints-da-api)
- [Testes](#testes)
- [CI/CD](#cicd)
- [Deploy no Render](#deploy-no-render)
- [Variáveis de Ambiente](#variáveis-de-ambiente)

---

## Visão Geral

URL.SHORT é um serviço de encurtamento de URLs com interface visual minimalista. Você cola uma URL longa, recebe um código curto de 6 caracteres, e consegue acompanhar quantas vezes o link foi acessado.

**Demo:** [url-shortener.onrender.com](https://url-shortener.onrender.com)

---

## Funcionalidades

- **Encurtamento de URLs** — gera códigos curtos de 6 caracteres alfanuméricos
- **Redirecionamento** — redireciona para a URL original com status 302
- **Estatísticas** — rastreia e exibe o número de acessos por link
- **Idempotência** — a mesma URL sempre retorna o mesmo código curto
- **Interface visual** — frontend minimalista servido pelo próprio FastAPI
- **Validação** — rejeita URLs inválidas com mensagens de erro claras
- **Histórico local** — links encurtados salvos no localStorage do browser

---

## Stack

| Camada | Tecnologia |
|---|---|
| API | FastAPI 0.111 |
| Banco de dados | PostgreSQL 16 + SQLAlchemy 2.0 |
| Validação | Pydantic v2 |
| Servidor | Uvicorn |
| Containerização | Docker + Docker Compose |
| Testes | pytest + SQLite in-memory |
| CI/CD | GitHub Actions |
| Deploy | Render |
| Frontend | HTML + CSS + JS puro |

---

## Arquitetura

```
Usuário
  │
  ├── POST /shorten ──────► FastAPI ──► PostgreSQL
  │                                         │
  ├── GET /{code} ◄────────────────── (busca URL)
  │       │
  │       └──► 302 Redirect ──► URL original
  │
  └── GET /stats/{code} ──► { access_count, created_at, ... }
```

**Fluxo de desenvolvimento:**

```
git push ──► GitHub Actions (testes + build) ──► Render (deploy automático)
```

---

## Estrutura do Projeto

```
url-shortener/
├── .github/
│   └── workflows/
│       └── ci.yml          # pipeline CI/CD
├── app/
│   ├── __init__.py
│   ├── main.py             # entrypoint FastAPI + rotas
│   ├── models.py           # modelos SQLAlchemy (URL, Access)
│   ├── schemas.py          # schemas Pydantic
│   ├── crud.py             # operações no banco
│   ├── database.py         # conexão e sessão
│   └── config.py           # variáveis de ambiente
├── frontend/
│   └── index.html          # interface visual
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # fixtures pytest
│   └── test_main.py        # 8 testes de integração
├── .env.example            # template de variáveis
├── .gitignore
├── conftest.py             # raiz do projeto para pytest
├── docker-compose.yml      # app + banco local
├── Dockerfile
├── pytest.ini
├── render.yaml             # configuração do Render
└── requirements.txt
```

---

## Como Rodar Localmente

### Pré-requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando

### 1. Clone o repositório

```bash
git clone https://github.com/SEU_USUARIO/url-shortener.git
cd url-shortener
```

### 2. Configure as variáveis de ambiente

```bash
cp .env.example .env
```

O `.env.example` já vem com os valores corretos para desenvolvimento local — não precisa alterar nada.

### 3. Suba os containers

```bash
docker compose up --build
```

Isso vai subir dois containers:
- **db** — PostgreSQL 16
- **app** — FastAPI com hot reload

### 4. Acesse

| Serviço | URL |
|---|---|
| Interface visual | http://localhost:8000 |
| Documentação API (Swagger) | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

Para rodar em background:

```bash
docker compose up --build -d
docker compose down  # para parar
```

---

## Endpoints da API

### `POST /shorten`

Encurta uma URL.

**Request:**
```json
{
  "original_url": "https://www.exemplo.com/url-muito-longa"
}
```

**Response `201`:**
```json
{
  "short_code": "aB3xKz",
  "short_url": "https://url-shortener.onrender.com/aB3xKz",
  "original_url": "https://www.exemplo.com/url-muito-longa",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### `GET /{short_code}`

Redireciona para a URL original.

**Response `302`:** redireciona para a URL original e registra o acesso.

**Response `404`:**
```json
{ "detail": "URL não encontrada" }
```

---

### `GET /stats/{short_code}`

Retorna estatísticas de acesso.

**Response `200`:**
```json
{
  "short_code": "aB3xKz",
  "original_url": "https://www.exemplo.com/url-muito-longa",
  "access_count": 42,
  "created_at": "2024-01-15T10:30:00Z",
  "is_active": true
}
```

---

### `GET /health`

Health check para monitoramento.

**Response `200`:**
```json
{ "status": "ok" }
```

---

## Testes

Os testes rodam com **SQLite em memória** — sem precisar de Docker ou PostgreSQL.

```bash
# ative o venv
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# instale as dependências
pip install -r requirements.txt

# rode os testes
pytest -v
```

**Cobertura dos testes:**

| Teste | O que valida |
|---|---|
| `test_health_check` | endpoint de health |
| `test_shorten_url` | encurtamento básico |
| `test_shorten_same_url_twice` | idempotência |
| `test_shorten_invalid_url` | validação de URL inválida |
| `test_redirect` | redirecionamento 302 |
| `test_redirect_not_found` | código inexistente retorna 404 |
| `test_stats` | contagem de acessos |
| `test_stats_not_found` | stats de código inexistente |

---

## CI/CD

O pipeline roda automaticamente em todo push para `main` ou `develop`, e em pull requests.

```
push/PR
  │
  ├── job: test
  │     ├── checkout
  │     ├── setup Python 3.11
  │     ├── pip install (com cache)
  │     └── pytest -v
  │
  └── job: build (só roda se test passar)
        ├── checkout
        └── docker build
```

**Configuração:** `.github/workflows/ci.yml`

**Regras de branch:**
- `main` — protegida, requer PR + CI verde para merge
- `develop` — branch de integração
- `feature/*` — branches de trabalho

---

## Deploy no Render

O deploy é automático a cada push na branch `main`.

### Configuração inicial

1. Crie um banco **PostgreSQL** no Render (free tier)
2. Crie um **Web Service** conectado a este repositório
   - Runtime: **Docker**
   - Branch: `main`
   - Start Command: `uvicorn app.main:app --host 0.0.0.0 --port 10000`
3. Configure as variáveis de ambiente (ver seção abaixo)

### Arquivo `render.yaml`

O projeto inclui `render.yaml` na raiz para configuração declarativa da infraestrutura.

---

## Variáveis de Ambiente

Copie `.env.example` para `.env` e preencha:

```env
# URL de conexão com o PostgreSQL
# Local (Docker): postgresql://postgres:postgres@db:5432/urlshortener
# Produção: fornecida pelo Render
DATABASE_URL=postgresql://postgres:postgres@db:5432/urlshortener

# Chave secreta da aplicação
# Gere com: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=troque-isso-em-producao

# URL base para geração dos links encurtados
BASE_URL=http://localhost:8000

# Comprimento do código gerado (padrão: 6)
CODE_LENGTH=6
```

> **Nunca** faça commit do arquivo `.env`. Ele já está no `.gitignore`.

---

<div align="center">

feito com FastAPI + PostgreSQL + Docker + GitHub Actions + Render

</div>