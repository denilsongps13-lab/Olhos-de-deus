# Olhos de Deus — análise inicial dos 7 projetos

Objetivo: construir o Olhos de Deus como projeto independente. O Mega Cérebro original não será alterado. Somente após o Olhos de Deus estar funcional e testado será criada uma cópia do Mega Cérebro para integração.

## 1. Graphify — Graphify-Labs/graphify (branch v8)
Licença detectada: Apache-2.0. Papel: inteligência estrutural do código. Pipeline observado: detect → extract → build → cluster → analyze → report → export. Usa AST/tree-sitter, grafo consultável, relações com confiança e suporte MCP/HTTP.

Aplicação no Olhos de Deus: criar um mapa interno do próprio projeto e, futuramente, mapear a cópia do Mega Cérebro antes da integração. Isso permitirá localizar módulos, dependências, ciclos e pontos de integração sem leitura cega de milhares de arquivos.

## 2. ComfyUI — Comfy-Org/ComfyUI (master)
Licença detectada: GPL-3.0. Papel estudado: motor de workflows em grafo/nós, fila assíncrona, reexecução parcial, subgrafos, templates, API e extensibilidade por nós.

Aplicação: aproveitar conceitos arquiteturais para um motor visual/modular de workflows do Olhos de Deus. Não copiar código GPL para o núcleo sem uma decisão explícita sobre implicações de licença.

## 3. Spec Kit — github/spec-kit (main)
Licença detectada: MIT. Papel: desenvolvimento orientado por especificação. Fluxo: constitution → specify → plan → tasks → implement → converge. Também possui assess e bug workflows.

Aplicação: tornar esse o protocolo de construção e evolução do Olhos de Deus. Toda função importante deverá nascer de especificação, plano, tarefas, implementação e validação.

## 4. QA Skills — petrkindlmann/qa-skills (main)
Licença detectada: MIT. Papel: biblioteca de 50 skills de QA/testes. Inclui unit, API, Playwright, segurança, performance, AI testing, bug reproduction, CI/CD, observabilidade e release readiness.

Aplicação: formar o Guardião/QA do Olhos de Deus. Mudanças relevantes devem passar por testes e critérios de qualidade antes de serem consideradas estáveis.

## 5. i-have-adhd — ayghri/i-have-adhd (main)
Licença detectada: MIT. Papel: camada de comunicação operacional para agentes — ação primeiro, passos numerados, sem tangentes e com próximo passo concreto. Possui integrações para diferentes coding agents.

Aplicação: criar um modo operacional conciso para agentes do Olhos de Deus e uma camada de adaptação de instruções entre runtimes.

## 6. Agency Agents — msitarzewski/agency-agents (main)
Licença detectada: MIT. Papel: catálogo amplo de agentes especializados organizados por divisões, incluindo arquitetura, backend, frontend, AI, DevOps, code review, knowledge graph e multi-agent systems.

Aplicação: usar o padrão de especialização para criar uma equipe menor e controlada do Olhos de Deus, evitando carregar centenas de agentes sem necessidade.

## 7. Artemis — google/artemis (main)
Licença detectada: Apache-2.0. Papel: automação Android em linguagem natural, execução observe-and-act, MCP, logs, screenshots, histórico comprimido, perfis rápidos/profundos e recuperação de ações bloqueadas.

Aplicação: criar futuramente um módulo Mobile Operator para testes e automações Android autorizadas, com trilha de execução e recuperação de falhas.

# Arquitetura proposta

Usuário/Interface
→ Orquestrador Central
→ Planejador (Spec Kit)
→ Roteador de Agentes (Agency Agents)
→ Skills/QA (QA Skills)
→ Knowledge Graph (Graphify)
→ Workflow Engine (conceitos ComfyUI)
→ Mobile Operator (Artemis)
→ Output/UX operacional (conceitos i-have-adhd)
→ Logs, auditoria e testes

# Primeiros agentes próprios

- ORCHESTRATOR: recebe a missão e decide o fluxo.
- ARCHITECT: especifica e planeja mudanças.
- CODEBASE_INTELLIGENCE: entende relações do código/grafo.
- BUILDER: implementa tarefas aprovadas pelo plano.
- GUARDIAN_QA: testa, revisa e bloqueia regressões.
- MOBILE_OPERATOR: executa/testa fluxos Android quando configurado.

# Regra para o Mega Cérebro

1. Desenvolver Olhos de Deus independentemente.
2. Torná-lo executável e testável.
3. Validar arquitetura e agentes.
4. Manter Mega Cérebro original intocado.
5. Criar cópia do Mega Cérebro.
6. Mapear a cópia com a camada de inteligência de código.
7. Integrar a cópia por módulos, com testes e rollback.
