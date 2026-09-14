$ErrorActionPreference = 'Stop'

Write-Host '== Olhos de Deus Windows build =='
python -m pip install --upgrade pip
python -m pip install -e '.[dev,desktop,build]'

Write-Host 'Running tests...'
python -m pytest -q

Write-Host 'Generating icon...'
python packaging/windows/make_icon.py

if (Test-Path dist) { Remove-Item dist -Recurse -Force }
if (Test-Path build/pyinstaller) { Remove-Item build/pyinstaller -Recurse -Force }

Write-Host 'Building desktop executable...'
python -m PyInstaller `
  --noconfirm `
  --clean `
  --windowed `
  --onedir `
  --name OlhosDeDeus `
  --icon build/OlhosDeDeus.ico `
  --workpath build/pyinstaller `
  --collect-all PySide6 `
  olhos_de_deus/desktop_entry.py

$env:QT_QPA_PLATFORM = 'offscreen'
Write-Host 'Running packaged smoke test...'
& .\dist\OlhosDeDeus\OlhosDeDeus.exe --smoke-test
if ($LASTEXITCODE -ne 0) {
  throw "Packaged smoke test failed with exit code $LASTEXITCODE"
}

Write-Host 'Windows executable ready: dist\OlhosDeDeus\OlhosDeDeus.exe'
