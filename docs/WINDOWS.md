# Olhos de Deus no Windows

## Entrega

O workflow `.github/workflows/windows-build.yml` executa em `windows-latest`, roda os testes, empacota a aplicacao desktop e monta o instalador.

Artefato esperado:

```text
OlhosDeDeus-Windows/
├── OlhosDeDeus-Setup.exe
└── SHA256SUMS.txt
```

O instalador usa Inno Setup e instala o programa em `Program Files\Olhos de Deus`, cria atalhos no Menu Iniciar e opcionalmente na Area de Trabalho.

## Dados do usuario

Arquivos que precisam de escrita ficam fora de `Program Files`:

```text
%LOCALAPPDATA%\OlhosDeDeus\
├── database\olhos_de_deus.db
├── logs\
├── config\
├── cache\
├── missions\
└── external\
```

Esses dados nao sao apagados automaticamente ao desinstalar para evitar perda acidental de historico.

## Interface

A aplicacao desktop usa PySide6/Qt e inclui:

- splash screen;
- dashboard em tema escuro/neon;
- olho/nucleo digital animado com estados idle, processando, sucesso e erro;
- central de missoes;
- telas das sete integracoes;
- System Doctor;
- bootstrap com preview antes de execucao real;
- logs persistentes e filtro;
- configuracoes de `EXTERNAL_ROOT`, `COMFYUI_URL` e dry-run;
- bandeja do Windows.

## Build local

Em Windows PowerShell, na raiz do repositorio:

```powershell
.\packaging\windows\build.ps1
```

Isso produz:

```text
dist\OlhosDeDeus\OlhosDeDeus.exe
```

Para compilar o instalador, instale Inno Setup 6 e execute:

```powershell
& "${env:ProgramFiles(x86)}\Inno Setup 6\ISCC.exe" installer\OlhosDeDeus.iss
```

Resultado:

```text
installer\output\OlhosDeDeus-Setup.exe
```

## Dependencias externas

O executavel inclui a interface e o runtime Python necessario ao Olhos de Deus, mas integracoes externas continuam refletindo dependencias reais:

- Graphify requer a CLI oficial `graphify` para execucao real;
- ComfyUI requer uma instancia/API acessivel;
- Spec Kit requer `specify` para execucao real;
- QA Skills, i-have-adhd e Agency Agents precisam estar presentes no `external` para carregar seus conteudos;
- Artemis requer seu runtime e um dispositivo/emulador Android quando a tarefa envolver o telefone.

A ausencia de uma dessas dependencias nao deve derrubar o aplicativo. O System Doctor mostra o estado real de cada fase.

## Seguranca operacional

As operacoes externas usam os adapters existentes e dry-run/preview quando aplicavel. A interface pede confirmacao antes de execucoes externas reais. Conteudo digitado pelo usuario nao e encaminhado a `shell=True`.
