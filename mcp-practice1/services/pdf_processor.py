import os
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from io import BytesIO
from typing import Any

class PDFProcessor:
    def __init__(self):
        endpoint = os.getenv("AZURE_FORM_RECOGNIZER_ENDPOINT")
        key = os.getenv("AZURE_FORM_RECOGNIZER_KEY")
        self.client = DocumentAnalysisClient(endpoint, AzureKeyCredential(key))

    def extract(self, pdf_path: str) -> dict[str, Any]:
        with open(pdf_path, "rb") as f:
            poller = self.client.begin_analyze_document("prebuilt-document", f)
        result = poller.result()
        return {
            "text": "\n".join([p.content for p in result.pages]),
            "tables": [
                [[cell.content for cell in row.cells] for row in tbl.rows]
                for tbl in result.tables
            ],
            "images": [img for img in result.images]  # metadata & bounding boxes
        }
