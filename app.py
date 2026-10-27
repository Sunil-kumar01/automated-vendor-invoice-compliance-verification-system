import os

import streamlit as st

from engine import analyze_document_locally, extract_text_from_pdf


st.set_page_config(page_title="Enterprise B2B AI Agent", layout="centered")

st.title("Secure Local B2B AI Agent")
st.write("Automated Vendor Invoice & Compliance Verification System")

uploaded_file = st.file_uploader("Upload Vendor Document (PDF)", type=["pdf"])

if uploaded_file is not None:
    temp_path = "temp.pdf"
    try:
        with open(temp_path, "wb") as file:
            file.write(uploaded_file.getbuffer())

        with st.spinner("Extracting text and running local AI validation..."):
            raw_text = extract_text_from_pdf(temp_path)
            agent_output = analyze_document_locally(raw_text)
    except Exception as error:
        st.error(f"Could not analyze this PDF: {error}")
    else:
        st.subheader("Extraction Results")
        st.json(agent_output)

        if agent_output.get("ComplianceStatus") == "Valid":
            st.success("Verification Passed: Invoice appears complete.")
        else:
            st.warning(
                "Attention Required: Discrepancies or missing compliance data found."
            )
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)
