from agents import function_tool

MEMORY = []

@function_tool
def save_memory(text: str, meta: str = "") -> dict:
    # Optionally, parse meta from JSON string if needed
    MEMORY.append({"text": text, "meta": meta})
    return {"status": "saved", "text": text[:100]}

@function_tool
def find_similar_memories(query: str, k: int = 3) -> dict:
    results = [{"text": m["text"][:100], "meta": m["meta"]} for m in MEMORY[-k:]]
    return {"query": query, "similar": results}


