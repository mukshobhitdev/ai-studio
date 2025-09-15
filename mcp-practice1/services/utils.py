def truncate_text(text, limit=1000):
    return text[:limit] + "..." if len(text) > limit else text
