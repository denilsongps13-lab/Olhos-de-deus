# Olhos de Deus

Central modular para agentes de IA, automacao, analise de codigo, QA e workflows. O nucleo e proprio; projetos externos ficam isolados e sao conectados por interfaces/adapters.

## Estado

Versao nativa atual: **0.3.0**.

Ja existe:
- orquestrador de missoes com estado e evidencia;
- planejador e roteador de agentes;
- gate final de QA;
- manifesto dos 7 projetos upstream;
- bootstrap seguro para clonar/atualizar os 7 repositorios em `external/`;
- adapters funcionais para as sete fases;
- comando `doctor` para readiness das integracoes;
- CLI instalavel e testes automatizados em GitHub Actions.

## As sete fases

1. Graphify — inteligencia estrutural de codigo via CLI oficial.
2. ComfyUI — integracao externa por HTTP API, mantendo o codigo GPL fora do nucleo.
3. Spec Kit — integracao com `specify-cli` para inicializacao spec-driven.
4. QA Skills — descoberta e carregamento de skills de QA.
5. i-have-adhd — perfil operacional de saida carregado do skill oficial.
6. Agency Agents — catalogo pesquisavel de agentes especializados.
7. Artemis — adapter CLI para automacao/testes Android autorizados.

Detalhes e requisitos de runtime: `docs/SEVEN_PHASES.md`.

## Projetos upstream

1. Graphify-Labs/graphify (`v8`, Apache-2.0)
2. Comfy-Org/ComfyUI (`master`, GPL-3.0)
3. github/spec-kit (`main`, MIT)
4. petrkindlmann/qa-skills (`main`, MIT)
5. ayghri/i-have-adhd (`main`, MIT)
6. msitarzewski/agency-agents (`main`, MIT)
7. google/artemis (`main`, Apache-2.0)

## Instalar

```bash
python -m pip install -e '.[dev]'
```

## Usar

Listar as fontes:

```bash
olhos-de-deus sources
```

Ver o bootstrap sem baixar nada:

```bash
olhos-de-deus bootstrap --dry-run
```

Baixar/atualizar todos os projetos externos:

```bash
olhos-de-deus bootstrap
```

Verificar as sete fases:

```bash
olhos-de-deus doctor
```

Testar tambem servicos externos configurados:

```bash
olhos-de-deus doctor --probe-services
```

Executar uma missao no nucleo:

```bash
olhos-de-deus run "Analisar erro no repositorio"
```

Tambem funciona por modulo:

```bash
python -m olhos_de_deus doctor --json
```

## Estrutura

- `olhos_de_deus/` — nucleo executavel, CLI e adapters
- `sources/` — manifesto, origem e licencas dos projetos estudados
- `external/` — clones locais gerados pelo bootstrap; nao entram no Git
- `tests/` — validacao automatizada
- `docs/` — arquitetura, analises e plano de integracao
- `core/` — documentacao arquitetural legada da fase inicial

## Regra de integracao

Nada e considerado integrado apenas por estar listado. Cada componente externo precisa de adapter, teste e limite de falha independente. Codigo de terceiros so entra no nucleo quando a licenca permitir e as atribuicoes forem preservadas.
