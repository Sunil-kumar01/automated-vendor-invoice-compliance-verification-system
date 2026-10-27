# Vendor Invoice Checker

## Explain it simply

**One line:** Upload a vendor invoice PDF and local AI reads its details and flags information that may need review.

The app is a small demo for checking vendor invoices before a person reviews them. It extracts invoice text, asks the AI to organize important fields, then displays the result. "Valid" is only an AI suggestion, not a financial approval.

## What model does it use?

It uses **Qwen 2.5**, served locally by **Ollama**. The app sends requests to `http://localhost:11434`; it does not send invoice text to a cloud AI service.

## What each file does

- `app.py` — Displays the page, accepts a PDF, and shows the analysis.
- `engine.py` — Extracts text from the PDF and asks local Qwen 2.5 to return invoice fields as JSON.
- `requirements.txt` — Lists the Python libraries needed to run the app.
- `.gitignore` — Keeps local Python environments, temporary PDFs, and caches out of Git.
- `README.md` — Explains the demo and how to start it.
- `venv/` — Python environment on this computer; it is not source code to share.

## How it works

1. A person uploads an invoice PDF.
2. `pypdf` reads the text from its pages.
3. The app sends the text to Qwen 2.5 through Ollama on this computer.
4. The model returns vendor, invoice, purchase order, amount, tax, line item, and issue fields as JSON.
5. The app displays the extracted data and marks it "Valid" or "Flagged" for a person to review.

Scanned/image-only PDFs may not contain selectable text, so this demo may not read them. It does not independently verify suppliers, purchase orders, arithmetic, or regulatory compliance.

## Start the demo on this Mac

Install Python and [Ollama](https://ollama.com/), then run these commands from the project folder:

```bash
ollama pull qwen2.5
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Open the **Local URL** shown in Terminal, usually `http://localhost:8501`. Keep Ollama running while you use the app.

## Let someone nearby try it

`localhost` only works on this computer. For someone on the same trusted Wi-Fi/LAN, start Streamlit so other devices can reach it:

```bash
streamlit run app.py --server.address 0.0.0.0
```

Find this Mac's local network IP address (for example, in **System Settings > Wi-Fi > Details**) and give the other person `http://<this-mac-ip>:8501`. Keep this limited to a trusted network, allow the connection through the Mac firewall if asked, and keep Ollama running. Do not expose this demo directly to the public internet; it has no login or access control.

For someone outside your network, `localhost` will not work. The simplest safe option is to show them the demo on this Mac; remote public sharing requires a separately secured hosting/tunnel setup.
