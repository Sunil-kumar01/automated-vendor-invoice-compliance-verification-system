# Run the Vendor Invoice Checker

Follow these steps on the computer where you want to try the demo.

## 1. Download and open the project

1. Download and extract the [project ZIP](https://github.com/Sunil-kumar01/automated-vendor-invoice-compliance-verification-system/archive/refs/heads/main.zip).
2. Open VS Code.
3. Choose **File > Open Folder** and select the extracted project folder. It should contain `app.py` and `requirements.txt`.

## 2. Install the two prerequisites

Install **Python 3** from [python.org](https://www.python.org/downloads/) and **Ollama** from [ollama.com/download](https://ollama.com/download). Keep an internet connection and at least 5 GB of free disk space for the AI model.

## 3. Start the app

In VS Code, choose **Terminal > New Terminal**. Run the command for your computer:

- **Windows:** `.\\run_windows.bat`
- **Mac:** `bash ./run_mac_linux.sh`

The launcher sets up the app's Python packages, starts Ollama if required, downloads Qwen 2.5 if it is not already installed, and launches the app. The initial model download is about 4.7 GB and can take several minutes.

## 4. Use the app

When Streamlit prints a **Local URL**, open it in a browser. It is usually [http://localhost:8501](http://localhost:8501). Upload a sample invoice PDF to try the extraction.

Keep the terminal and Ollama running while using the app. To stop the app, focus the VS Code terminal and press **Ctrl+C**.

## What is included and what is installed separately?

The ZIP includes the app source, setup scripts, Python package list, README, and guide PDF. Python, Ollama, and the Qwen 2.5 model are installed on each computer; the model is not bundled because it is several gigabytes. The app runs locally and is not published to the public internet.

Use sample, non-sensitive invoices only. This is a demo; its AI result is for human review and is not a financial or compliance approval.

## If it does not start

- If `ollama` or `python` is not recognized, install that prerequisite and restart VS Code.
- If setup pauses while downloading Qwen, wait for the download to finish.
- If the app says Ollama cannot be reached, open the Ollama app and run the launcher again.
- On Mac, if the shell blocks the launcher, run `chmod +x run_mac_linux.sh` in the VS Code terminal and retry `bash ./run_mac_linux.sh`.
