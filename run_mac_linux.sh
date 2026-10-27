#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")"

if ! command -v python3 >/dev/null 2>&1; then
    echo "Python 3 is required. Install it from https://www.python.org/downloads/"
    exit 1
fi

if ! command -v ollama >/dev/null 2>&1; then
    echo "Ollama is required. Install it from https://ollama.com/download"
    exit 1
fi

if ! curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null; then
    echo "Starting Ollama..."
    ollama serve >/tmp/vendor-invoice-ollama.log 2>&1 &
    for attempt in $(seq 1 30); do
        if curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null; then
            break
        fi
        sleep 1
    done
fi

if ! curl -fsS --max-time 2 http://127.0.0.1:11434/api/tags >/dev/null; then
    echo "Ollama did not start. Open the Ollama app and try again."
    exit 1
fi

if ! ollama list | grep -q 'qwen2.5'; then
    echo "Downloading Qwen 2.5 (about 4.7 GB; this may take a while)..."
    ollama pull qwen2.5
fi

if [ ! -x ".venv/bin/python" ]; then
    python3 -m venv .venv
fi

.venv/bin/python -m pip install -r requirements.txt
exec .venv/bin/python -m streamlit run app.py
