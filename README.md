# Olhos de Deus

Central modular para agentes de IA, automacao, analise de codigo, QA e workflows. O nucleo e proprio; projetos externos ficam isolados e sao conectados por interfaces/adapters.

## Estado

Versao atual: **0.5.0**.

Ja existe:
- aplicativo desktop nativo para Windows com PySide6;
- dashboard escuro/neon com nucleo visual animado;
- central de missoes ligada ao orquestrador;
- telas das sete integracoes, System Doctor, logs e configuracoes;
- persistencia local SQLite em `%LOCALAPPDATA%\OlhosDeDeus`;
- suporte a bandeja do Windows e splash screen;
- build com PyInstaller e instalador com Inno Setup;
- orquestrador de missoes com estado e evidencia;
- planejador, roteador de agentes e Guardian QA;
- bootstrap seguro dos sete projetos externos;
- CLI e testes automatizados em Linux/Windows.

## Windows

O fluxo de entrega gera o artefato **OlhosDeDeus-Windows**, contendo:

- `OlhosDeDeus-Setup.exe`
- `SHA256SUMS.txt`

Depois de instalado, o uso normal acontece pela interface grafica, sem precisar abrir PowerShell ou CMD. O instalador cria atalhos e inclui o runtime Python necessario dentro do aplicativo empacotado.

Dados gravaveis nao ficam em `Program Files`. Banco, logs, cache, configuracoes e clones externos ficam em:

```text
%LOCALAPPDATA%\OlhosDeDeus
```

Detalhes de build e instalacao: `docs/WINDOWS.md`.

Para desenvolvimento local:

```powershell
python -m pip install -e '.[dev,desktop]'
olhos-de-deus-desktop
```

## As sete fases

1. Graphify — inteligencia estrutural de codigo via CLI oficial.
2. ComfyUI — integracao externa por HTTP API, mantendo o codigo GPL fora do nucleo.
3. Spec Kit — integracao com `specify-cli` para inicializacao spec-driven.
4. QA Skills — descoberta e carregamento de skills de QA.
5. i-have-adhd — perfil operacional de saida carregado do skill oficial.
6. Agency Agents — catalogo pesquisavel de agentes especializados.
7. Artemis — adapter CLI para automacao/testes Android autorizados.

A interface mostra o estado real. Se um runtime, servico ou dispositivo nao existir, ele aparece como `PENDING`, `INSTALLED` ou offline; a tela nao simula sucesso.

Detalhes das integracoes: `docs/SEVEN_PHASES.md`.

## Projetos upstream

1. Graphify-Labs/graphify (`v8`, Apache-2.0)
2. Comfy-Org/ComfyUI (`master`, GPL-3.0)
3. github/spec-kit (`main`, MIT)
4. petrkindlmann/qa-skills (`main`, MIT)
5. ayghri/i-have-adhd (`main`, MIT)
6. msitarzewski/agency-agents (`main`, MIT)
7. google/artemis (`main`, Apache-2.0)

## CLI

Instalar o nucleo para desenvolvimento:

```bash
python -m pip install -e '.[dev]'
```

Preparar os repositorios externos:

```bash
olhos-de-deus bootstrap
```

Verificar o estado das sete fases:

```bash
olhos-de-deus doctor
```

Executar/consultar cada fase. Por seguranca, as fases que executam ferramentas externas usam dry-run por padrao; adicione `--execute` somente quando quiser executar de verdade.

```bash
olhos-de-deus phase graphify .
olhos-de-deus phase comfyui --probe
olhos-de-deus phase spec-kit .
olhos-de-deus phase qa-skills
olhos-de-deus phase i-have-adhd
olhos-de-deus phase agency-agents
olhos-de-deus phase artemis "Open Settings"
```

## Estrutura

- `olhos_de_deus/` — nucleo executavel, CLI e adapters
- `olhos_de_deus/desktop/` — interface Windows, controller e persistencia
- `packaging/windows/` — build do executavel e geracao do icone
- `installer/` — projeto do instalador Inno Setup
- `sources/` — manifesto, origem e licencas dos projetos estudados
- `external/` — clones locais; nao entram no Git
- `tests/` — validacao automatizada
- `docs/` — arquitetura, integracoes e operacao

## Regra de integracao

Nada e considerado integrado apenas por estar listado. Cada componente externo precisa de adapter, teste e limite de falha independente. Codigo de terceiros so entra no nucleo quando a licenca permitir e as atribuicoes forem preservadas. ComfyUI permanece isolado como servico externo devido a GPL-3.0.
