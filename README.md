# Flashcards Micro-API (MVP)

Micro-API em Python para um app de flashcards inspirado no Anki, com foco em criação rápida de cards e suporte a adição assistida por LLM (ex.: conteúdo em português e inglês).

## Objetivo

Entregar um backend simples, evolutivo e pronto para integração com clientes web/mobile, cobrindo:

- CRUD básico de decks e cards
- Suporte a cards bilíngues (PT/EN)
- Pipeline inicial para gerar/sugerir cards via LLM
- Base para evolução de revisão espaçada e analytics

## Stack

- **Linguagem:** Python 3.12
- **Framework API:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Ambiente virtual:** `.venv`
- **Dependências:** `requirements.txt` com versões fixas (`==`)

## Como rodar localmente

### 1) Pré-requisitos

- Python 3.12 instalado

### 2) Configuração do ambiente

No diretório do projeto:

```bash
/usr/bin/python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

### 3) Subir a API

Com a aplicação em `app/main.py`:

```bash
.venv/bin/uvicorn app.main:app --reload
```

API disponível em:

- `http://127.0.0.1:8000`
- Docs Swagger: `http://127.0.0.1:8000/docs`
- Docs ReDoc: `http://127.0.0.1:8000/redoc`

## Roadmap de releases

### v0.1.0 — Fundação da API (MVP técnico)

- Estrutura inicial do projeto
- Setup de ambiente e dependências fixas
- Endpoint de health check
- Padrão base de resposta/erro

### v0.2.0 — Core de flashcards

- CRUD de decks
- CRUD de cards
- Campos para frente/verso e idioma (`pt`, `en`)
- Filtros simples por deck/idioma

### v0.3.0 — Integração inicial com LLM

- Endpoint para sugerir cards a partir de texto livre
- Estratégia de validação/sanitização de entrada
- Registro de origem do card (manual vs LLM)

### v0.4.0 — Revisão e aprendizado

- Modelo inicial de revisão espaçada
- Histórico de respostas (acerto/erro)
- Priorização de cards para revisão

### v0.5.0 — Qualidade e operação

- Testes automatizados (unitários/integrados)
- Logs estruturados e observabilidade básica
- Containerização e checklist de deploy

## Status

Projeto em fase inicial de MVP.
