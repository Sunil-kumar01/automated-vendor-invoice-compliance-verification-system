@echo off
setlocal
cd /d "%~dp0"

where py >nul 2>nul
if errorlevel 1 (
    echo Python 3 is required. Install it from https://www.python.org/downloads/
    pause
    exit /b 1
)

where ollama >nul 2>nul
if errorlevel 1 (
    echo Ollama is required. Install it from https://ollama.com/download
    pause
    exit /b 1
)

powershell -NoProfile -ExecutionPolicy Bypass -Command "$u='http://127.0.0.1:11434/api/tags'; try { Invoke-RestMethod $u -TimeoutSec 2 | Out-Null } catch { Start-Process -FilePath 'ollama' -ArgumentList 'serve' -WindowStyle Hidden; for($i=0;$i -lt 30;$i++){ Start-Sleep -Seconds 1; try { Invoke-RestMethod $u -TimeoutSec 2 | Out-Null; exit 0 } catch {} }; Write-Error 'Ollama did not start'; exit 1 }"
if errorlevel 1 (
    echo Ollama did not start. Open the Ollama app and try again.
    pause
    exit /b 1
)

ollama list | findstr /I "qwen2.5" >nul
if errorlevel 1 (
    echo Downloading Qwen 2.5 (about 4.7 GB; this may take a while)...
    ollama pull qwen2.5
    if errorlevel 1 (
        pause
        exit /b 1
    )
)

if not exist ".venv\Scripts\python.exe" py -3 -m venv .venv
if errorlevel 1 (
    echo Could not create the Python environment.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo Could not install Python dependencies.
    pause
    exit /b 1
)

".venv\Scripts\python.exe" -m streamlit run app.py
pause
