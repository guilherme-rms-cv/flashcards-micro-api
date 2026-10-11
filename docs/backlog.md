# Backlog mínimo do MVP

## Release 1 — Core

- [ ] RF-01 — Criar deck
  - Descrição: permitir a criação de um deck com nome e descrição opcional.
  - Critério de aceite:
    - [ ] `POST /decks` aceita payload com `name` e `description` opcional.
    - [ ] retorna `201 Created` com identificador do deck.
    - [ ] rejeita payload sem `name` com `400 Bad Request`.

- [ ] RF-02 — Listar decks
  - Descrição: consultar todos os decks cadastrados.
  - Critério de aceite:
    - [ ] `GET /decks` retorna lista em JSON.
    - [ ] cada item inclui `id`, `name`, `description` e `created_at`.
    - [ ] resposta é vazia (`[]`) quando não existem decks.

- [ ] RF-03 — Buscar deck por ID
  - Descrição: consultar um deck específico.
  - Critério de aceite:
    - [ ] `GET /decks/{id}` retorna o deck correto.
    - [ ] retorna `404 Not Found` para identificador inexistente.

- [ ] RF-04 — Atualizar deck
  - Descrição: alterar nome e/ou descrição do deck.
  - Critério de aceite:
    - [ ] `PUT /decks/{id}` atualiza os campos enviados.
    - [ ] retorna `200 OK` com deck atualizado.
    - [ ] rejeita atualização com `name` vazio.

- [ ] RF-05 — Excluir deck
  - Descrição: remover um deck do sistema.
  - Critério de aceite:
    - [ ] `DELETE /decks/{id}` remove o deck.
    - [ ] retorna `204 No Content` em sucesso.
    - [ ] retorna `404` ao tentar excluir deck inexistente.

- [ ] RF-06 — Criar card em deck
  - Descrição: permitir adicionar um card a um deck existente.
  - Critério de aceite:
    - [ ] `POST /decks/{deck_id}/cards` aceita `front`, `back`, `language` e `source`.
    - [ ] associa o card ao deck informado.
    - [ ] retorna `201 Created` com o card persistido.

- [ ] RF-07 — Listar cards por deck
  - Descrição: consultar todos os cards de um deck.
  - Critério de aceite:
    - [ ] `GET /decks/{deck_id}/cards` retorna lista de cards do deck.
    - [ ] cards fora do deck não aparecem na resposta.
    - [ ] retorna `404` quando o deck não existe.

- [ ] RF-08 — Atualizar card
  - Descrição: editar frente, verso e idioma de um card.
  - Critério de aceite:
    - [ ] `PUT /cards/{id}` atualiza campos válidos.
    - [ ] rejeita campos obrigatórios vazios.
    - [ ] retorna `404` para cartão inexistente.

- [ ] RF-09 — Excluir card
  - Descrição: remover um card individual.
  - Critério de aceite:
    - [ ] `DELETE /cards/{id}` remove o card.
    - [ ] retorna `204` em sucesso.
    - [ ] retorna `404` para card inexistente.

- [ ] RT-01 — Estrutura base da API
  - Descrição: configurar aplicação FastAPI com rotas e organização mínima por módulos.
  - Critério de aceite:
    - [ ] projeto inicia com `uvicorn app.main:app`.
    - [ ] `/health` responde `200 OK`.
    - [ ] endpoints ficam organizados em módulos ou arquivos coerentes.

## Release 2 — Qualidade

- [ ] RT-02 — Validação de entrada
  - Descrição: validar payloads e campos obrigatórios antes da persistência.
  - Critério de aceite:
    - [ ] entradas inválidas retornam `400 Bad Request`.
    - [ ] mensagens de erro são coerentes e legíveis.
    - [ ] não há persistência de dados inconsistentes.

- [ ] RF-10 — Suporte a cards bilíngues
  - Descrição: permitir cards com frente e verso em idiomas distintos.
  - Critério de aceite:
    - [ ] aceita `language` ou variantes de idioma como `en`, `pt`.
    - [ ] estrutura do card mantém `front` e `back` corretamente preenchidos.
    - [ ] exemplo típico de inglês/português funciona sem erro.

- [ ] RF-11 — Registrar origem do card
  - Descrição: marcar se o card foi criado manualmente ou por LLM.
  - Critério de aceite:
    - [ ] `source` pode ser `manual` ou `llm`.
    - [ ] criação por LLM preserva a origem correta.
    - [ ] resposta da API expõe o campo `source`.

- [ ] RT-03 — Tratamento de erros padronizado
  - Descrição: padronizar respostas de erro da API.
  - Critério de aceite:
    - [ ] erros seguem contrato JSON consistente.
    - [ ] recursos inexistentes retornam `404` com detalhe claro.
    - [ ] erros de validação retornam `400` com mensagens resumidas.

- [ ] RT-04 — Documentação OpenAPI
  - Descrição: disponibilizar documentação automática da API.
  - Critério de aceite:
    - [ ] Swagger está disponível em `/docs`.
    - [ ] endpoints principais aparecem corretamente documentados.
    - [ ] payloads e respostas são legíveis para integração.

- [ ] RF-12 — Criar cards em lote no deck
  - Descrição: permitir criação de 1..N cards em uma única requisição, incluindo cards gerados por LLM.
  - Critério de aceite:
    - [ ] `POST /decks/{deck_id}/cards/bulk` aceita payload com `cards` (array com pelo menos 1 item).
    - [ ] cada item de `cards` exige `front`, `back`, `language` e `source`.
    - [ ] `source` aceita apenas `manual` ou `llm`.
    - [ ] operação persiste todos os cards válidos no deck informado.
    - [ ] operação rejeita payload sem cards com `400 Bad Request`.

- [ ] RF-13 — Validar contrato de card de integração com LLM
  - Descrição: garantir compatibilidade do contrato da API com JSON de cards retornado por LLM.
  - Critério de aceite:
    - [ ] a API aceita o formato `{ "cards": [ { "front": "...", "back": "...", "language": "en", "source": "llm" } ] }`.
    - [ ] o campo `deck_id` é aceito pelo path (`/decks/{deck_id}/...`) ou opcionalmente no payload, conforme regra documentada.
    - [ ] em caso de item inválido, a API retorna erro padronizado e não persiste dados inconsistentes.

## Release 3 — Entrega final

- [ ] RT-05 — Observabilidade mínima
  - Descrição: garantir monitoramento básico da aplicação.
  - Critério de aceite:
    - [ ] `/health` indica disponibilidade da API.
    - [ ] logs de operações principais são registrados.
    - [ ] falhas de integração com LLM são tratadas de forma explícita.

- [ ] RT-06 — Configuração e ambiente de execução
  - Descrição: preparar ambiente para execução local e homologação.
  - Critério de aceite:
    - [ ] `requirements.txt` está definido com dependências fixas.
    - [ ] README contém instruções de instalação e execução.
    - [ ] aplicação pode ser iniciada via `uvicorn` sem configuração manual complexa.

- [ ] RF-14 — Fluxo end-to-end de criação de deck e cards
  - Descrição: validar a operação completa do MVP em um cenário realista.
  - Critério de aceite:
    - [ ] usuário consegue criar deck.
    - [ ] usuário consegue adicionar cards ao deck.
    - [ ] usuário consegue adicionar múltiplos cards em lote com endpoint bulk.
    - [ ] usuário consegue listar e consultar os itens criados.
    - [ ] o fluxo funciona sem erros de consistência.

- [ ] RF-15 — Entrega final do MVP
  - Descrição: consolidar produto no estado mínimo viável para demonstração.
  - Critério de aceite:
    - [ ] API principal funcionando em ambiente local.
    - [ ] documentação inicial disponível.
    - [ ] backlog e critérios de aceite atendidos para as releases entregues.

## Status geral

- [ ] Release 1 concluída
- [ ] Release 2 concluída
- [ ] Release 3 concluída
