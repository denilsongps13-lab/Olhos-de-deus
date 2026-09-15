# Ruflo — Fase 0 opcional

O Ruflo (`ruvnet/ruflo`, MIT) entra no Olhos de Deus como **meta-harness opcional**, sem substituir as sete fases existentes.

## Papel

```text
Usuario
  -> Olhos de Deus
    -> Ruflo (fase 0 / meta-harness)
      -> fases 1..7
      -> agentes
      -> memoria / MCP / workflows do Ruflo quando configurados
```

As sete fases continuam sendo Graphify, ComfyUI, Spec Kit, QA Skills, Output Profile, Agency Agents e Artemis.

## Integracao segura

O codigo do Ruflo nao e copiado para o nucleo. O adapter `olhos_de_deus.ruflo.RufloAdapter` usa os comandos oficiais via `npx` e executa subprocessos sem `shell=True`.

Nenhuma instalacao acontece silenciosamente. `init` e dry-run por padrao no CLI e no controller desktop.

## Requisitos

- Node.js
- `npx`
- acesso ao npm apenas quando o usuario escolher executar Ruflo de verdade

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

Isso evita mostrar sucesso falso apenas porque Node.js esta instalado.

## Proximos passos

A v0.6 estabelece o boundary seguro, diagnostico e inicializacao. A delegacao real de missoes ao Ruflo/MCP deve ser adicionada somente apos validar os comandos e o ciclo de vida do servidor no Windows, sem transformar texto do usuario diretamente em comando de shell.
