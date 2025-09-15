from agents import function_tool

SAMPLE_PAPERS = [
    {"title": "Fast Optical Flow in Deep Networks", "authors": ["A. Researcher"], "summary": "A fast method for optical flow."},
    {"title": "Efficient Transformer Variants", "authors": ["B. Scientist"], "summary": "Transformer speedups via pruning."},
]

@function_tool
def search_papers(query: str) -> dict:
    matches = [p for p in SAMPLE_PAPERS if query.lower() in (p["title"] + " " + p["summary"]).lower()]
    if not matches:
        matches = SAMPLE_PAPERS[:2]
    return {"query": query, "matches": matches}

@function_tool
def summarize_text(text: str, max_sentences: int = 3) -> dict:
    sentences = text.split(".")
    summary = ". ".join(sentences[:max(1, min(len(sentences), max_sentences))]).strip()
    return {"summary": summary or text[:200]}

@function_tool
def fetch_statistics(topic: str) -> dict:
    return {"topic": topic, "papers_found": 42, "hotness_score": 0.78}
