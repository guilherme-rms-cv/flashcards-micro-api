# Flashcards Micro-API (MVP)

Micro-API em Python para gestão de decks e cards de flashcards, com suporte a criação em lote.

## Objetivo do release atual

Entregar uma API REST simples e estável para:

- CRUD de decks;
- CRUD de cards;
- criação em lote de cards por deck em `POST /decks/{deck_id}/cards/bulk`;
- exclusão em cascata de cards ao remover um deck.

> Integração interna com LLM para geração de cards não faz parte deste release.

## Stack

- **Linguagem:** Python 3.12
- **Framework:** FastAPI
- **Servidor ASGI:** Uvicorn
- **Modelagem/validação:** Pydantic v2
- **Persistência:** SQLite

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
source .venv/bin/activate
.venv/bin/uvicorn app.main:app --reload
```

Documentação automática:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Health check:

- `GET /health`

## Testes

Executar toda a suíte:

```bash
.venv/bin/python -m pytest -q
```

Executar apenas API tests:

```bash
.venv/bin/python -m pytest tests/api -q
```

Executar apenas validações de modelo:

```bash
.venv/bin/python -m pytest tests/models -q
```

## Arquitetura

A aplicação segue arquitetura em camadas:

- **API**: rotas HTTP e mapeamento de status/erros;
- **Service**: regras de negócio;
- **Repository**: acesso ao SQLite;
- **Models**: contratos Pydantic.

Referências:

- [app/main.py](./app/main.py)
- [app/api/deck_routes.py](./app/api/deck_routes.py)
- [app/api/card_routes.py](./app/api/card_routes.py)
- [app/services/deck_service.py](./app/services/deck_service.py)
- [app/services/card_service.py](./app/services/card_service.py)
- [app/repositories/deck_repository.py](./app/repositories/deck_repository.py)
- [app/repositories/card_repository.py](./app/repositories/card_repository.py)
- [app/models/deck.py](./app/models/deck.py)
- [app/models/card.py](./app/models/card.py)
- [docs/arquitetura-componentes.mmd](./docs/arquitetura-componentes.mmd)

## Contrato da API (estado atual)

### Decks

- `GET /decks`
- `POST /decks`
- `GET /decks/{deck_id}`
- `PUT /decks/{deck_id}` (atualização parcial permitida)
- `DELETE /decks/{deck_id}` (`204` em sucesso, `404` se não existir)

Exemplo de criação:

```bash
curl -X POST "http://127.0.0.1:8000/decks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "English Phrases",
    "description": "Frases para revisão diária"
  }'
```

### Cards

- `GET /cards`
- `POST /cards`
- `GET /cards/{card_id}`
- `PUT /cards/{card_id}` (atualização parcial permitida)
- `DELETE /cards/{card_id}` (`204` em sucesso, `404` se não existir)

Exemplo de criação:

```bash
curl -X POST "http://127.0.0.1:8000/cards" \
  -H "Content-Type: application/json" \
  -d '{
    "front": "I review flashcards every morning.",
    "back": "Eu reviso flashcards toda manhã.",
    "source": "manual",
    "deck_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"
  }'
```

### Bulk por deck

- `POST /decks/{deck_id}/cards/bulk`

Regras:

- `deck_id` existe **somente no path**;
- body contém apenas `cards`;
- cada item de `cards` exige `front`, `back` e `source` (`manual` ou `llm`);
- operação é transacional (all-or-nothing).

Exemplo válido:

```bash
curl -X POST "http://127.0.0.1:8000/decks/<deck_id>/cards/bulk" \
  -H "Content-Type: application/json" \
  -d '{
    "cards": [
      {
        "front": "Data quality is as important as model quality.",
        "back": "A qualidade dos dados é tão importante quanto a qualidade do modelo.",
        "source": "manual"
      },
      {
        "front": "Small iterative improvements lead to robust systems.",
        "back": "Pequenas melhorias iterativas levam a sistemas robustos.",
        "source": "llm"
      }
    ]
  }'
```

## Erros e status HTTP

### Principais códigos

- `201 Created`: criação com sucesso (`POST /decks`, `POST /cards`, `POST bulk`);
- `200 OK`: leitura/atualização com sucesso;
- `204 No Content`: exclusão com sucesso;
- `400 Bad Request`: regra de negócio inválida;
- `404 Not Found`: recurso não encontrado;
- `422 Unprocessable Entity`: erro de validação de schema/payload.

### Exemplos de erro

Deck inexistente:

```json
{
  "detail": "Deck '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."
}
```

Card inexistente:

```json
{
  "detail": "Card '3fa85f64-5717-4562-b3fc-2c963f66afa6' not found."
}
```

`POST /cards` sem `deck_id`:

```json
{
  "detail": "deck_id is required to create a card"
}
```

`PUT /cards/{card_id}` com payload vazio:

```json
{
  "detail": "at least one field must be provided for card update"
}
```

Validação de payload (`422`), exemplo de `source` inválido:

```json
{
  "detail": [
    {
      "loc": ["body", "cards", 0, "source"],
      "msg": "Input should be 'manual' or 'llm'",
      "type": "literal_error"
    }
  ]
}
```

## Integridade de dados

- cards possuem chave estrangeira para deck;
- exclusão de deck executa **cascade delete** no banco;
- após `DELETE /decks/{deck_id}`, não permanecem cards órfãos.

## Documentação complementar

- [docs/escopo-mvp.md](./docs/escopo-mvp.md)
- [docs/backlog.md](./docs/backlog.md)
