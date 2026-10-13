# Flashcards Micro-API (MVP)

Micro-API em Python para um app de flashcards inspirado no Anki.  
O foco do MVP é oferecer um backend simples, evolutivo e pronto para integração com clientes web/mobile.

## Objetivo

Entregar a base funcional para:

- gestão de decks;
- criação e manutenção de cards;
- integração opcional com LLM para geração de cards;
- criação em lote de cards (bulk), incluindo payloads vindos de IA.

## Stack

- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Modelagem/validação:** Pydantic v2
- **Persistência inicial:** SQLite (sem dependências externas de banco)

## Instalação

### Pré-requisitos

- Python 3.12

### Setup do ambiente

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Execução

```bash
.venv/bin/uvicorn app.main:app --reload
```

Endpoints de documentação:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Health check:

- `GET /health`

## Testes

O projeto já possui testes iniciais de API e validação de modelos em `tests/`.

### Executar todos os testes

```bash
.venv/bin/python -m pytest -q
```

### Executar apenas testes de API

```bash
.venv/bin/python -m pytest tests/api -q
```

### Executar apenas validações de modelo

```bash
.venv/bin/python -m pytest tests/models -q
```

> Observação: se `pytest` não estiver instalado no ambiente local, instale com:
>
> ```bash
> .venv/bin/pip install pytest
> ```

## Arquitetura

A aplicação segue arquitetura em camadas:

- **API**: rotas HTTP e mapeamento de status/erros;
- **Service**: regras de negócio;
- **Repository**: acesso ao SQLite;
- **Models**: contratos Pydantic.

Estrutura atual:

- [app/main.py](./app/main.py)
- [app/api/deck_routes.py](./app/api/deck_routes.py)
- [app/services/deck_service.py](./app/services/deck_service.py)
- [app/repositories/deck_repository.py](./app/repositories/deck_repository.py)
- [app/models/deck.py](./app/models/deck.py)

Diagrama de componentes:

- [docs/arquitetura-componentes.mmd](./docs/arquitetura-componentes.mmd)

Escopo e backlog:

- [docs/escopo-mvp.md](./docs/escopo-mvp.md)
- [docs/backlog.md](./docs/backlog.md)

## Usabilidade da API (estado atual)

Rotas de **Decks** implementadas:

- `GET /decks`
- `POST /decks`
- `GET /decks/{deck_id}`
- `PUT /decks/{deck_id}`
- `DELETE /decks/{deck_id}`

### Exemplo de criação de deck

```bash
curl -X POST "http://127.0.0.1:8000/decks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "English Phrases",
    "description": "Frases para revisão diária"
  }'
```

### Exemplo de atualização parcial

```bash
curl -X PUT "http://127.0.0.1:8000/decks/<deck_id>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "English Phrases - Avançado"
  }'
```

## Limitações atuais

- CRUD completo de **cards** ainda não foi implementado;
- endpoint de **bulk cards** está definido no escopo/arquitetura, mas ainda não está disponível;
- integração com LLM é apenas prevista (não implementada no core);
- sem autenticação/autorização;
- persistência SQLite local (sem migrações formais);
- sem pipeline de CI e sem cobertura de testes consolidada.

## Próximos passos

1. Implementar `CardRepository`, `CardService` e rotas de cards.
2. Implementar `POST /decks/{deck_id}/cards/bulk` com contrato `cards: []`.
3. Padronizar payload de erro para além de 404 (ex.: 400 e 500).
4. Adicionar suíte de testes para cards, bulk e cenários de erro de persistência.
5. Incluir `pytest` e demais dependências de desenvolvimento em arquivo dedicado.
6. Evoluir observabilidade (logs estruturados e métricas básicas).

## Status do projeto

MVP em evolução ativa, com fundação de Decks concluída e próximos incrementos focados em Cards, bulk import e qualidade operacional.
