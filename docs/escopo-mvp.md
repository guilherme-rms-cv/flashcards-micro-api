# Escopo do MVP: Micro-API de Flashcards

## 1. Objetivo

Desenvolver uma micro-API em Python para suportar um aplicativo de flashcards inspirado no Anki, com foco em criação rápida de cards, organização por decks e auxílio de geração de conteúdo por LLM. O MVP deve permitir que usuários cadastrem, consultem, atualizem e removam decks e flashcards, além de oferecer uma rota inicial de sugestão de cards baseada em texto livre, priorizando simplicidade, integração fácil e evolução incremental.

O produto deve funcionar como base de backend para uma interface web ou mobile, com API REST padronizada, documentação clara e arquitetura mínima, mas extensível. A solução não tem como objetivo substituir o ecossistema completo de revisão espaçada e aprendizagem ativa do Anki em sua forma completa; o escopo do MVP é entregar a base operacional e funcional para criação e gestão de conteúdo de estudo.

## 2. Visão geral do produto

A API gerencia:

- decks (conjuntos de cards organizados por tema ou assunto);
- cards (itens de estudo com frente e verso, idioma e metadados básicos);
- importação/criação em lote de cards no formato JSON, com origem `manual` ou `llm`;
- organização e consulta simples de conteúdo por deck, idioma e status.

A experiência principal do usuário é:

- criar um deck;
- adicionar cards manualmente ou por geração externa de IA (LLM) em lote;
- listar e consultar cards por critérios simples;
- editar ou remover entradas quando necessário;
- usar a API como base para uma camada frontend ou integração futura.

## 3. Requisitos funcionais

### 3.1 Gestão de decks

1. O sistema deve permitir a criação de um novo deck com nome e descrição opcional.
2. O sistema deve permitir a listagem de todos os decks cadastrados.
3. O sistema deve permitir a consulta de um deck por identificador único.
4. O sistema deve permitir a atualização do nome e da descrição de um deck existente.
5. O sistema deve permitir a exclusão de um deck, com regra de consistência que evite remoção indevida de dados relacionados.
6. O sistema deve manter a associação de cards a decks, garantindo que cada card pertença a pelo menos um deck.

### 3.2 Gestão de cards

1. O sistema deve permitir a criação de cards com campos mínimos de frente, verso e idioma.
2. O sistema deve suportar cards bilíngues, com exemplos típicos de frente em inglês e verso em português.
3. O sistema deve permitir a listagem de todos os cards de um deck.
4. O sistema deve permitir a consulta de um card por identificador único.
5. O sistema deve permitir a atualização de conteúdo do card, incluindo frente, verso, idioma e metadata relevante.
6. O sistema deve permitir a exclusão de um card individual.
7. O sistema deve possibilitar filtros simples por deck, idioma e status operacional, quando aplicável.
8. O sistema deve registrar origem do card, diferenciando `manual` e `llm`.
9. O sistema deve permitir criação em lote de cards por deck via endpoint dedicado.
10. O endpoint de lote deve aceitar payload no formato `{ "cards": [ ... ] }` com pelo menos 1 card.
11. Cada item do lote deve conter `front`, `back`, `language` e `source`.
12. O sistema deve validar que `source` aceita apenas `manual` ou `llm`.
13. O `deck_id` deve ser aceito no path (`/decks/{deck_id}/cards/bulk`) e opcionalmente no payload, conforme regra de API definida.

### 3.3 Fluxo de criação assistida por LLM

1. O MVP deve suportar integração com LLM como fonte opcional de conteúdo para criação de cards.
2. A responsabilidade da API é receber e validar o JSON final de cards, sem exigir componente interno de sugestão no núcleo.
3. A resposta usada da LLM deve ser compatível com o contrato `{ "cards": [ { "front": "...", "back": "...", "language": "en", "source": "llm" } ] }`.
4. O sistema deve permitir persistir 1..N cards dessa resposta em um deck específico por operação em lote.
5. O sistema deve rejeitar payloads com cards vazios, campos ausentes ou formato inválido.
6. O sistema deve registrar origem `llm` quando o card vier de geração externa.
7. O fluxo de geração textual/prompts pode ser tratado fora da API principal e evoluído em versões futuras.

### 3.4 Consulta e organização

1. O sistema deve permitir a busca por cards por deck.
2. O sistema deve permitir a listagem de cards por idioma, quando houver múltiplos idiomas na base.
3. O sistema deve retornar respostas estruturadas em JSON, com campos explícitos e status HTTP adequado.
4. O sistema deve disponibilizar documentação automática da API via Swagger/OpenAPI.

### 3.5 Tratamento de erros e consistência

1. O sistema deve responder com erros padronizados para validação, recurso inexistente e conflitos de integridade.
2. O sistema deve rejeitar entradas inválidas antes da persistência.
3. O sistema deve evitar que cards ou decks sejam criados com dados inconsistentes ou incompletos.
4. O sistema deve apresentar mensagens de erro em linguagem técnica clara e sem vazamento excessivo de detalhes sensíveis.

## 4. Requisitos não funcionais

### 4.1 Desempenho

1. A API deve responder em tempo adequado para operações básicas de CRUD, considerando volume inicial de uso de um MVP.
2. O tempo de resposta para listagens simples e consultas por identificador deve ser viável para uso em ambiente local ou de homologação.
3. A geração de cards via LLM deve ser tratada como operação assíncrona ou de baixo volume inicial, sem bloquear a API em cenários normais.

### 4.2 Disponibilidade e confiabilidade

1. O sistema deve ser resiliente a falhas de entrada e processamento simples.
2. O sistema deve oferecer tratamento explícito para erros de integração com serviços externos, como LLMs.
3. O sistema deve manter consistência mínima dos dados em operações de criação, atualização e remoção.

### 4.3 Segurança

1. A API deve validar todos os dados recebidos antes do processamento.
2. O sistema deve impedir uso indevido de entrada maliciosa em campos de texto e prompts.
3. O sistema deve seguir boas práticas de separação entre dados de usuário, prompts e artefatos gerados.
4. O sistema deve evitar exposição de informações sensíveis em logs e respostas de erro.

### 4.4 Manutenibilidade

1. O código deve seguir uma estrutura modular e escalável, separando rotas, serviços, modelos e utilitários.
2. A API deve ser documentada por OpenAPI/Swagger para facilitar uso e integração por desenvolvedores.
3. O projeto deve permitir evolução para novos módulos sem reescrita completa da base.

### 4.5 Observabilidade

1. O sistema deve registrar logs de operações principais de criação, leitura, atualização e exclusão.
2. O sistema deve permitir monitoramento básico de saúde da aplicação.
3. O sistema deve expor métricas ou endpoints de verificação de disponibilidade mínimos para operação local e em ambiente de teste.

### 4.6 Escalabilidade

1. A arquitetura deve permitir crescimento futuro de decks, cards e integrações sem necessidade de mudança estrutural radical.
2. O MVP deve ser construído de modo que suporte a expansão para novas entidades, como revisão espaçada, histórico de estudo e analytics.
3. A camada de LLM deve ser desacoplada o suficiente para permitir troca de provedor ou estratégia futura.

## 5. Requisitos de negócio e uso

- O usuário principal do MVP é um estudante ou profissional que deseja registrar conceitos e revisar conteúdo rapidamente.
- O processo de criação de cards deve reduzir a fricção de inserção manual de conteúdo.
- A integração com LLM deve acelerar a geração de cards a partir de textos, listas, materiais de estudo e resumos.
- O sistema deve se adaptar a uso local e em ambiente de desenvolvimento, não exigindo infraestrutura complexa no início.

## 6. Fora de escopo do MVP

Os seguintes itens não fazem parte do escopo do MVP e devem ser tratados em versões posteriores:

1. Sistema completo de revisão espaçada com algoritmos avançados de intervalo de repetição.
2. Analytics detalhados de desempenho do usuário, incluindo métricas de acerto/erro por assunto, dia ou categoria.
3. Gamificação, ranking, conquistas, badges e elementos sociais.
4. Sincronização multi-dispositivo com autenticação avançada e gerenciamento de sessão.
5. Suporte a múltiplos usuários com acesso isolado, autorização por roles e segredos de ambiente complexos.
6. Sistema de colaboração em decks ou compartilhamento de conteúdo entre usuários.
7. Geração de cards com qualidade de produção e prompt engineering sofisticado em larga escala.
8. Tradução automática de alta qualidade para múltiplos idiomas com pós-processamento editorial.
9. Integração com IA multimodal, incluindo imagens, áudio, vídeo e OCR.
10. Cronogramas de estudo personalizados, recomendações inteligentes e decisões adaptativas de ensino.
11. Exportação/importação avançada de conteúdo em formatos empresariais ou interoperabilidade com outros sistemas de estudo.
12. Observabilidade de nível produção com dashboards completos, alertas automatizados e tracing distribuído.
13. Autenticação de usuários, autorização por permissão e gestão de chaves de acesso para clientes externos.
14. Containerização em produção, orchestration e deploy em Kubernetes.
15. Mecanismo de backup, restauração e retenção de dados em nível enterprise.

## 7. Critérios de sucesso do MVP

O MVP será considerado adequado se:

- permitir criação e consulta de decks e cards de forma estável;
- permitir criação de múltiplos cards em uma única operação (`bulk`);
- suportar uso básico de cards bilíngues;
- aceitar contrato JSON de cards gerados por LLM no endpoint de lote;
- manter a API documentada e de fácil integração;
- apresentar estrutura extensível para evoluções futuras.

## 8. Resumo executivo

Este MVP entrega uma base funcional para um aplicativo de flashcards com foco em organização de conteúdo e criação de cards de forma simples e escalável. O objetivo central é reduzir o esforço de criação manual, mantendo a arquitetura enxuta (API, Service e Repository) e extensível. A solução cobre o núcleo de gestão de decks e cards, inclui criação em lote com contrato JSON compatível com conteúdo gerado por LLM e estabelece uma base sólida para evoluções futuras.
