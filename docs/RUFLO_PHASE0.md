# Ruflo — Fase 0 opcional

O Ruflo (`ruvnet/ruflo`, MIT) entra no Olhos de Deus como **meta-harness opcional**, sem substituir as sete fases existentes.

## Papel

```text
Usuario
  -> Olhos de Deus
    -> Ruflo (fase 0 / meta-harness)
      -> swarm / coordenacao multiagente
      -> fases 1..7
      -> agentes
      -> memoria / MCP / workflows do Ruflo quando configurados
```

As sete fases continuam sendo Graphify, ComfyUI, Spec Kit, QA Skills, Output Profile, Agency Agents e Artemis.

## Integracao segura

O codigo do Ruflo nao e copiado para o nucleo. O adapter `olhos_de_deus.ruflo.RufloAdapter` usa os comandos oficiais via `npx` e executa subprocessos sem `shell=True`.

Nenhuma instalacao acontece silenciosamente. Inicializacao e comandos de swarm usam dry-run/preview quando aplicavel e a interface pede confirmacao antes da execucao real.

Entradas de topologia, estrategia e permissoes usam allowlists. O objetivo do swarm e passado como um unico argumento de subprocesso, nunca como texto de shell.

## Requisitos

- Node.js
- `npx`
- acesso ao npm apenas quando o usuario escolher executar Ruflo de verdade
- runtime de agente/LLM configurado separadamente para execucao autonoma real

## CLI

Status local:

```bash
olhos-de-deus ruflo status --workspace .
```

Ver o comando que seria usado para inicializar:

```bash
olhos-de-deus ruflo init --workspace .
```

Executar a inicializacao oficial nao interativa:

```bash
olhos-de-deus ruflo init --workspace . --execute
```

Usar o wizard oficial:

```bash
olhos-de-deus ruflo init --workspace . --wizard --execute
```

Ver o comando do servidor MCP sem iniciar um processo permanente:

```bash
olhos-de-deus ruflo mcp --workspace .
```

Consultar a versao via `npx`:

```bash
olhos-de-deus ruflo probe --workspace . --execute
```

## Swarm no Windows

A v0.6.1 adiciona controles visuais para:

- escolher topologia (`hierarchical`, `mesh`, `ring`, `star`, `hybrid`, `hierarchical-mesh`, `pheromone-adaptive`);
- escolher estrategia;
- escolher preset de permissoes;
- limitar a quantidade de agentes (1 a 15 no Olhos de Deus);
- visualizar o comando antes de executar;
- criar a topologia de swarm;
- consultar o estado real do swarm;
- coordenar um objetivo via `ruflo swarm start`.

O painel mostra stdout/stderr reais e nao marca a execucao de um LLM como concluida apenas porque o Ruflo criou/coordenou o swarm. Segundo a arquitetura do Ruflo, a execucao efetiva do modelo depende do runtime/agente configurado (por exemplo Claude Code/Codex ou outro mecanismo suportado).

## System Doctor

O doctor tradicional continua reportando exatamente as sete fases. Para acrescentar a fase 0:

```bash
olhos-de-deus doctor --with-ruflo --ruflo-workspace .
```

Na interface Windows, o controller inclui o Ruflo como linha `0` do System Doctor, mantendo a metrica principal das sete integracoes separada.

## Estado READY

O adapter considera o Ruflo `READY` quando:

1. `node` e `npx` estao disponiveis; e
2. o workspace possui `.claude-flow`, criado pela inicializacao do Ruflo.

O estado de swarm e detectado separadamente por `.swarm/state.json`. Isso evita mostrar sucesso falso apenas porque Node.js esta instalado.

## Limite atual

A v0.6.1 implementa o boundary seguro, diagnostico, inicializacao e coordenacao de swarm. O proximo passo para autonomia completa e ligar um runtime de agente/LLM suportado e gerenciar seu ciclo de vida sem transformar texto do usuario diretamente em comando de shell.
