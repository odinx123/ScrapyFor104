param(
    [string]$PythonVersion = "3.11.9"
)

$ErrorActionPreference = "Stop"

$PyenvCommand = Get-Command pyenv -ErrorAction SilentlyContinue
if (-not $PyenvCommand) {
    $PyenvRoot = Join-Path $env:USERPROFILE ".pyenv\pyenv-win"
    $PyenvBin = Join-Path $PyenvRoot "bin"
    $PyenvShims = Join-Path $PyenvRoot "shims"
    $PyenvBat = Join-Path $PyenvBin "pyenv.bat"

    if (-not (Test-Path $PyenvBat)) {
        throw "pyenv was not found. Install pyenv-win to $PyenvRoot, then rerun this script."
    }

    $env:PYENV = $PyenvRoot
    $env:PYENV_ROOT = $PyenvRoot
    $env:PYENV_HOME = $PyenvRoot
    $env:PATH = "$PyenvBin;$PyenvShims;$env:PATH"
}

pyenv install -s $PythonVersion
pyenv local $PythonVersion

python -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\pip.exe install -r requirements.txt

Write-Host "Environment ready. Activate with: .\.venv\Scripts\Activate.ps1"
