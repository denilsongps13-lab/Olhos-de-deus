#define MyAppName "Olhos de Deus"
#define MyAppVersion "0.6.2"
#define MyAppPublisher "Olhos de Deus"
#define MyAppExeName "OlhosDeDeus.exe"

[Setup]
AppId={{AF09F8D5-1297-4B9A-8C89-2C9EC0E3B63B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Olhos de Deus
DefaultGroupName=Olhos de Deus
DisableProgramGroupPage=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
OutputDir=output
OutputBaseFilename=OlhosDeDeus-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
SetupIconFile=..\build\OlhosDeDeus.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
VersionInfoVersion=0.6.2.0
VersionInfoDescription=Olhos de Deus - Central de Inteligência Artificial

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Atalhos:"; Flags: checkedonce

[Files]
Source: "..\dist\OlhosDeDeus\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\Olhos de Deus"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\Olhos de Deus"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir Olhos de Deus"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

; Dados, logs e banco ficam em %LOCALAPPDATA%\OlhosDeDeus e não são apagados
; pelo desinstalador para evitar perda acidental do histórico do usuário.
