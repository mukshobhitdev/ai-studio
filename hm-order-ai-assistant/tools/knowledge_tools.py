from agents import function_tool
from data.knowledge_data import knowledge_data


@function_tool
def get_knowledge_by_topic(topic: str) -> dict:
    """
    Retrieve a knowledge entry by its topic.
    Args:
        topic (str): The topic to search for.
    Returns:
        dict: The knowledge entry if found, else an empty dict.
    """
    for entry in knowledge_data:
        if entry["topic"].lower() == topic.lower():
            return entry
    return {}

@function_tool
def search_knowledge_by_keyword(keyword: str) -> list:
    """
    Search for knowledge entries by (partial) keyword match in topic or summary (case-insensitive).
    Args:
        keyword (str): The (partial) keyword to search for.
    Returns:
        list: List of matching knowledge entries.
    """
    return [k for k in knowledge_data if keyword.lower() in k["topic"].lower() or keyword.lower() in k["summary"].lower()]

@function_tool
def list_all_knowledge() -> list:
    """
    List all available knowledge entries.
    Returns:
        list: All knowledge entries in the database.
    """
    return knowledge_data
