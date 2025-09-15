from agents import function_tool
from .research_tools import summarize_text

@function_tool
def extract_entities(text: str) -> dict:
    return {"text_preview": text[:100], "entities": [{"type": "PERSON", "text": "Alice"}, {"type": "ORG", "text": "OpenAI"}]}

@function_tool
def compare_documents(doc1: str, doc2: str) -> dict:
    return {"doc1_summary": summarize_text(doc1)["summary"], "doc2_summary": summarize_text(doc2)["summary"], "diff": "Differences (demo)"}
