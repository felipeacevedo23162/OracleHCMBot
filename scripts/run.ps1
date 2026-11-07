$ErrorActionPreference = "Stop"
if (-not (Test-Path .\.venv\Scripts\python.exe)) {
    throw "Ejecute scripts\setup_windows.ps1 primero."
}
& .\.venv\Scripts\python.exe main.py
