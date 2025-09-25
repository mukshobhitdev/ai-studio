from agents import function_tool

MEMORY = []

@function_tool
def save_memory(text: str, meta: str = "") -> dict:
    MEMORY.append({"text": text, "meta": meta})
    return {"status": "saved", "text": text[:100]}

@function_tool
def find_similar_memories(query: str, k: int = 3) -> dict:
    results = [{"text": m["text"][:100], "meta": m["meta"]} for m in MEMORY[-k:]]
    return {"query": query, "similar": results}

@function_tool
def find_all_memories(query: str, k: int = 13) -> dict:
    """Return all short term memories.

    Args:
        query: The query to find similar memories.
        k: The number of similar memories to return.
    """
    results = [{"text": m["text"], "meta": m["meta"]} for m in MEMORY]
    return {"query": query, "all_memories": results}
