# Sete fases de integracao

O Olhos de Deus trata cada projeto upstream como uma fase independente. A fase so e considerada operacional quando o adapter consegue detectar o runtime ou o conteudo necessario sem misturar codigo de terceiros no nucleo.

## Fase 1 — Graphify

Objetivo: inteligencia estrutural da base de codigo.

Adapter: `GraphifyAdapter`.

Contrato atual: detecta a CLI oficial `graphify`, monta o comando de analise e permite execucao real ou `dry_run`.

Requisito de runtime: pacote oficial `graphifyy` instalado e comando `graphify` no PATH.

## Fase 2 — ComfyUI

Objetivo: workflows visuais e geracao multimodal.

Adapter: `ComfyUIAdapter`.

Contrato atual: mantem o ComfyUI fora do nucleo GPL, testa a API externa e envia workflows em formato de API para `POST /prompt`.

Requisito de runtime: uma instancia do ComfyUI rodando; por padrao `http://127.0.0.1:8188` ou `COMFYUI_URL`.

## Fase 3 — Spec Kit

Objetivo: especificacao e planejamento antes da implementacao.

Adapter: `SpecKitAdapter`.

Contrato atual: detecta `specify` e inicializa um projeto em modo nao interativo usando o fluxo oficial do Spec Kit.

Requisito de runtime: `specify-cli` instalado.

## Fase 4 — QA Skills

Objetivo: carregar skills de teste e qualidade.

Adapter: `QASkillsAdapter`.

Contrato atual: descobre `skills/*/SKILL.md`, lista skills e carrega a skill pedida.

Requisito de runtime: repositorio `qa-skills` clonado pelo bootstrap.

## Fase 5 — i-have-adhd

Objetivo: camada de saida operacional curta e orientada a acao.

Adapter: `ADHDOutputAdapter`.

Contrato atual: carrega o arquivo oficial `skills/i-have-adhd/SKILL.md` para que o runtime de agentes possa aplicar o perfil de comunicacao.

Requisito de runtime: repositorio `i-have-adhd` clonado pelo bootstrap.

## Fase 6 — Agency Agents

Objetivo: catalogo de agentes especializados.

Adapter: `AgencyAgentsAdapter`.

Contrato atual: descobre definicoes de agentes em Markdown, lista agentes e busca/carrega um agente por nome.

Requisito de runtime: repositorio `agency-agents` clonado pelo bootstrap.

## Fase 7 — Artemis

Objetivo: operacao e testes Android autorizados.

Adapter: `ArtemisAdapter`.

Contrato atual: valida o checkout do Artemis, detecta `uv` e monta/executa `uv run artemis run <tarefa> --profile flash|pro`.

Requisito de runtime: Artemis clonado, `uv` instalado e aparelho/emulador Android configurado para a execucao real.

## Doctor

Use:

```bash
olhos-de-deus doctor
```

Para JSON:

```bash
olhos-de-deus doctor --json
```

Para testar tambem servicos externos como ComfyUI:

```bash
olhos-de-deus doctor --probe-services
```

O modo `--strict` encerra com erro quando qualquer fase nao estiver operacional, servindo como gate de readiness em ambientes preparados.
