import os
from mcp.server.fastmcp import FastMCP
from service.pdf_processor import PDFProcessor
from service.search_indexer import SearchIndexer

mcp = FastMCP("pdf_tool")

processor = PDFProcessor()
indexer = SearchIndexer()

@mcp.tool()
def load_pdf(path: str) -> dict:
    """Extract pdf content (text, tables, images metadata)"""
    return processor.extract(path)

@mcp.tool()
def index_pdf(path: str) -> str:
    """Load PDF and index its text in Azure Search."""
    data = processor.extract(path)
    doc_id = os.path.basename(path)
    indexer.index_doc(doc_id, data["text"])
    return f"Indexed {doc_id}"

if __name__ == "__main__":
    mcp.run()
