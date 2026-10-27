import json
import urllib.error
import urllib.request

from pypdf import PdfReader


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5"


def extract_text_from_pdf(pdf_file_path):
    """Extract selectable text from a PDF using pypdf."""
    reader = PdfReader(pdf_file_path)
    text_parts = []

    for page_number, page in enumerate(reader.pages, start=1):
        page_text = page.extract_text() or ""
        if page_text.strip():
            text_parts.append(f"--- Page {page_number} ---\n{page_text}")

    return "\n\n".join(text_parts).strip()


def analyze_document_locally(raw_text):
    """Extract invoice information using the local Qwen 2.5 model in Ollama."""
    if not raw_text or not raw_text.strip():
        return {
            "VendorName": "",
            "InvoiceNumber": "",
            "InvoiceDate": "",
            "PO_Number": "",
            "Currency": "",
            "Subtotal": "",
            "Tax": "",
            "TotalAmount": "",
            "LineItems": [],
            "ComplianceStatus": "Flagged",
            "Issues": ["No readable text was extracted from the document."],
            "SummaryNotes": (
                "The document could not be analyzed because no readable text was found."
            ),
        }

    prompt = f"""
You are an automated B2B invoice and document extraction agent.

Read the document text and extract information accurately.

IMPORTANT RULES:
1. Do not invent information.
2. If a field is not present, return an empty string.
3. Extract values exactly from the document whenever possible.
4. Return ONLY valid JSON.
5. Do not add explanations outside the JSON.

Return this exact JSON structure:

{{
    "VendorName": "",
    "InvoiceNumber": "",
    "InvoiceDate": "",
    "PO_Number": "",
    "Currency": "",
    "Subtotal": "",
    "Tax": "",
    "TotalAmount": "",
    "LineItems": [
        {{
            "Description": "",
            "Quantity": "",
            "UnitPrice": "",
            "Amount": ""
        }}
    ],
    "ComplianceStatus": "",
    "Issues": [],
    "SummaryNotes": ""
}}

FIELD DEFINITIONS:

VendorName:
The company or vendor that issued the invoice.

InvoiceNumber:
The invoice number or invoice ID.

InvoiceDate:
The invoice date.

PO_Number:
The purchase order number, if present.

Currency:
Currency such as INR, USD, EUR, GBP, etc.

Subtotal:
Invoice subtotal before tax.

Tax:
Tax amount shown on the invoice.

TotalAmount:
Final invoice amount payable.

LineItems:
Extract each invoice line item. For every item include Description, Quantity,
UnitPrice, and Amount.

ComplianceStatus:
Use "Valid" when the document appears complete and contains expected invoice
information. Use "Flagged" when information is missing, unclear, or inconsistent.

Issues:
List specific missing or suspicious information, such as a missing invoice date,
missing PO number, missing total, or unclear tax information.

SummaryNotes:
Provide a short summary of what was found.

DOCUMENT TEXT:

{raw_text}
"""

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "format": "json",
    }

    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            response_data = response.read().decode("utf-8")

        result = json.loads(response_data)
        model_response = result.get("response", "").strip()

        if not model_response:
            return {
                "ComplianceStatus": "Flagged",
                "Issues": ["Local AI model returned an empty response."],
                "SummaryNotes": "No analysis was returned by Qwen 2.5.",
            }

        return json.loads(model_response)

    except json.JSONDecodeError as error:
        return {
            "ComplianceStatus": "Flagged",
            "Issues": ["The AI returned an invalid JSON response."],
            "SummaryNotes": f"JSON parsing error: {error}",
        }
    except urllib.error.URLError as error:
        return {
            "ComplianceStatus": "Flagged",
            "Issues": ["Could not connect to the local Ollama server."],
            "SummaryNotes": f"Ollama connection error: {error}",
        }
    except Exception as error:
        return {
            "ComplianceStatus": "Flagged",
            "Issues": ["Unexpected error occurred during document analysis."],
            "SummaryNotes": str(error),
        }
