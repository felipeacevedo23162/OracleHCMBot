$ErrorActionPreference = "Stop"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "No se encontró el lanzador 'py'. Instale Python 3.12 o superior."
}

py -3.12 -m venv .venv
& .\.venv\Scripts\python.exe -m pip install --upgrade pip
& .\.venv\Scripts\python.exe -m pip install -r requirements.txt
& .\.venv\Scripts\python.exe -m playwright install
& .\.venv\Scripts\python.exe scripts\create_excel_template.py
& .\.venv\Scripts\python.exe main.py
Write-Host "Instalación completada. Microsoft Edge debe estar instalado para uso real."
