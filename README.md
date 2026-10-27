# Vendor Invoice Checker

## Explain it simply

**One line:** Upload a vendor invoice PDF and the app uses AI to read the details and point out information that may need review.

The app extracts invoice text, asks an AI model to organize the details, and displays the result. Its "Valid" or "Flagged" result is a first-pass suggestion, not a financial approval.

## Project files (one line each)

- `app.py` — Shows the upload page, sends the PDF for analysis, and displays the result.
- `engine.py` — Reads PDF text and calls the selected AI service to extract invoice details.
- `requirements.txt` — Lists the Python packages Streamlit Cloud installs.
- `.gitignore` — Keeps local environments, caches, and secret settings out of Git.
- `.streamlit/secrets.toml.example` — Safe template showing which AI settings to add in Streamlit Cloud.
- `README.md` — Explains the project and how to run and publish it.
- `venv/` — Local Python setup; do not upload it to GitHub.

## AI model

The original local setup uses **Qwen 2.5 through Ollama**. For cloud deployment, configure an **OpenAI-compatible AI service** in Streamlit Cloud Secrets. Set its endpoint, model name, and API key there; never put the real key in this repository. This supports cloud AI providers that implement the OpenAI chat-completions API and JSON response format.

Invoice text is sent to the AI service configured for the app. Check your organization's privacy rules and the provider's data policy before uploading real invoices.

## Run locally on macOS

1. Install Python and [Ollama](https://ollama.com/).
2. In Terminal, download the model and start Ollama:

   ```bash
   ollama pull qwen2.5
   ```

3. In the project folder, create an environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

5. Open `http://localhost:8501` and upload a text-readable PDF.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository and upload the project files. Include `app.py`, `engine.py`, `requirements.txt`, `README.md`, `.gitignore`, and `.streamlit/secrets.toml.example`. Do not upload `venv/`, `.venv/`, private invoices, or a real `secrets.toml`.
2. In [Streamlit Community Cloud](https://share.streamlit.io/), choose **Create app**, select the GitHub repository and branch, and set the main file to `app.py`.
3. In the app's **Settings > Secrets**, add settings for an OpenAI-compatible provider. Use the provider's own endpoint, model name, and key:

   ```toml
   AI_PROVIDER = "openai_compatible"
   AI_MODEL = "your-provider-model-name"
   OPENAI_BASE_URL = "https://your-provider.example/v1"
   OPENAI_API_KEY = "your-secret-api-key"
   ```

4. Save the settings and deploy. Upload a test invoice and review the result before sharing the app.

The cloud app cannot reach Ollama at `localhost` on your computer. Do not select `AI_PROVIDER = "ollama"` in Community Cloud unless Ollama is running at a cloud-accessible URL and `OLLAMA_URL` is set to that URL. An OpenAI-compatible cloud provider is the straightforward option. Provider usage may cost money; check its pricing and limits.
