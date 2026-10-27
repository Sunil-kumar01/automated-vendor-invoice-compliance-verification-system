# Vendor Invoice Checker

## Explain it simply

**One line:** Upload a vendor invoice PDF and local AI reads its details and flags information that may need review.

The app is a small demo for checking vendor invoices before a person reviews them. It extracts invoice text, asks the AI to organize important fields, then displays the result. "Valid" is only an AI suggestion, not a financial approval.

For a simple use-case, workflow, file-by-file, and video explanation guide, see [Vendor Invoice Demo Guide (PDF)](./Vendor_Invoice_Demo_Guide_2026-10-27.pdf).

## What model does it use?

It uses **Qwen 2.5**, served locally by **Ollama**. The app sends requests to `http://localhost:11434`; it does not send invoice text to a cloud AI service.

## What each file does

- `app.py` — Displays the page, accepts a PDF, and shows the analysis.
- `engine.py` — Extracts text from the PDF and asks local Qwen 2.5 to return invoice fields as JSON.
- `requirements.txt` — Lists the Python libraries needed to run the app.
- `run_windows.bat` / `run_mac_linux.sh` — One-click setup and app launchers.
- `.gitignore` — Keeps local Python environments, temporary PDFs, and caches out of Git.
- `README.md` — Explains the demo and how to start it.
- `.venv/` — Python environment created on each computer; it is not included in the download.

## How it works

1. A person uploads an invoice PDF.
2. `pypdf` reads the text from its pages.
3. The app sends the text to Qwen 2.5 through Ollama on this computer.
4. The model returns vendor, invoice, purchase order, amount, tax, line item, and issue fields as JSON.
5. The app displays the extracted data and marks it "Valid" or "Flagged" for a person to review.

Scanned/image-only PDFs may not contain selectable text, so this demo may not read them. It does not independently verify suppliers, purchase orders, arithmetic, or regulatory compliance.

## Run the demo on Windows or Mac

Install Python 3 and [Ollama](https://ollama.com/download), then open the extracted project folder in VS Code. In the VS Code Explorer, run `run_windows.bat` on Windows or `run_mac_linux.sh` on Mac/Linux. On Mac/Linux, you may first need to run `chmod +x run_mac_linux.sh` from the VS Code terminal.

The launcher creates a local Python environment, installs the packages from `requirements.txt`, starts Ollama if needed, downloads Qwen 2.5 if it is missing, and starts Streamlit. The first run needs internet access and several GB of free disk space for the AI model; allow time for the model download.

Alternatively, in the VS Code terminal from the project folder run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
ollama pull qwen2.5
streamlit run app.py
```

On Windows PowerShell, use `py -3 -m venv .venv`, then `.venv\\Scripts\\python.exe -m pip install -r requirements.txt`, `ollama pull qwen2.5`, and `.venv\\Scripts\\python.exe -m streamlit run app.py`.

Open the **Local URL** shown in the terminal, usually `http://localhost:8501`. Keep Ollama running while using the app. The ZIP includes the app source and Python dependency list, but not Python, Ollama, or the multi-GB Qwen model; each computer installs these locally.

## Let someone nearby try it

`localhost` only works on this computer. For someone on the same trusted Wi-Fi/LAN, start Streamlit so other devices can reach it:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Find this computer's local network IP address and give the other person `http://<computer-ip>:8501`. Keep this limited to a trusted network, allow the connection through the firewall if asked, and keep Ollama running. Do not expose this demo directly to the public internet; it has no login or access control.

## Temporary sharing over another network

A Cloudflare Quick Tunnel can temporarily provide a public HTTPS link to this computer's running Streamlit app. Qwen 2.5 and Ollama continue to run on this computer. Start Ollama and Streamlit, then in a second terminal run:

```bash
cloudflared tunnel --url http://127.0.0.1:8501
```

Share the `https://...trycloudflare.com` link printed in the terminal. Keep the terminal open while testing and stop the tunnel with **Ctrl+C** when finished. Anyone with the link can access the app, which has no login. Use only sample, non-sensitive invoices. Never expose Ollama's port (`11434`) directly. This is temporary demo access, not production deployment.
