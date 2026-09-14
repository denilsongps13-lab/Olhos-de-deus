# Olhos de Deus

Central modular para agentes de IA, automacao, analise de codigo, QA e workflows. O nucleo e proprio; projetos externos ficam isolados e sao conectados por interfaces/adapters.

## Estado

Versao nativa atual: **0.2.0**.

Ja existe:
- orquestrador de missoes com estado e evidencia;
- planejador e roteador de agentes;
- gate final de QA;
- manifesto dos 7 projetos upstream;
- bootstrap seguro para clonar/atualizar os 7 repositorios em `external/`;
- CLI instalavel;
- testes automatizados em GitHub Actions.

## Projetos upstream

1. Graphify-Labs/graphify (`v8`, Apache-2.0)
2. Comfy-Org/ComfyUI (`master`, GPL-3.0)
3. github/spec-kit (`main`, MIT)
4. petrkindlmann/qa-skills (`main`, MIT)
5. ayghri/i-have-adhd (`main`, MIT)
6. msitarzewski/agency-agents (`main`, MIT)
7. google/artemis (`main`, Apache-2.0)

O ComfyUI permanece como integracao externa por causa da GPL-3.0; seu codigo nao e copiado para o nucleo nativo.

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

Baixar apenas uma integracao:

```bash
olhos-de-deus bootstrap artemis
```

Executar uma missao no nucleo:

```bash
olhos-de-deus run "Analisar erro no repositorio"
```

Tambem funciona por modulo:

```bash
python -m olhos_de_deus sources
```

## Estrutura

- `olhos_de_deus/` — nucleo executavel e CLI
- `sources/` — manifesto, origem e licencas dos projetos estudados
- `external/` — clones locais gerados pelo bootstrap; nao entram no Git
- `tests/` — validacao automatizada
- `docs/` — arquitetura, analises e plano de integracao
- `core/` — documentacao arquitetural legada da fase inicial

## Regra de integracao

Nada e considerado integrado apenas por estar listado. Cada componente externo deve ter adapter, teste e limite de falha independente antes de ser promovido para uso de producao. Codigo de terceiros so entra no nucleo quando a licenca permitir e as atribuicoes forem preservadas.
