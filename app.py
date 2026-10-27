import os

import streamlit as st
from pypdf.errors import PdfReadError

from engine import analyze_document, extract_text_from_pdf


def setting(name, default=""):
    return str(st.secrets.get(name, os.environ.get(name, default)))


st.set_page_config(page_title="Vendor Invoice Checker", layout="centered")
st.title("Vendor Invoice Checker")
st.write("Upload a vendor invoice PDF to extract key details and flag items for review.")
st.caption(
    "Invoice text is sent to the AI service configured for this app. "
    "Only upload documents approved for that service."
)

uploaded_file = st.file_uploader("Upload vendor invoice (PDF)", type=["pdf"])

if uploaded_file is not None:
    provider = setting("AI_PROVIDER", "ollama")
    model = setting("AI_MODEL", "qwen2.5")
    ollama_url = setting("OLLAMA_URL", "http://localhost:11434/api/generate")
    openai_base_url = setting("OPENAI_BASE_URL")
    api_key = setting("OPENAI_API_KEY")

    try:
        with st.spinner("Reading the invoice and checking its details..."):
            raw_text = extract_text_from_pdf(uploaded_file.getvalue())
            agent_output = analyze_document(
                raw_text,
                provider=provider,
                model=model,
                ollama_url=ollama_url,
                openai_base_url=openai_base_url,
                api_key=api_key,
            )
    except (PdfReadError, OSError, RuntimeError, ValueError) as error:
        st.error(f"Could not analyze this PDF: {error}")
    else:
        st.subheader("Extraction results")
        st.json(agent_output)

        if agent_output.get("ComplianceStatus") == "Valid":
            st.success("The invoice appears complete. Please review before approval.")
        else:
            st.warning("Review the flagged or missing information before approval.")
