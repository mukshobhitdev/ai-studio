from data.order_followup_data import order_followup_data
from agents import function_tool

@function_tool
def get_followup_by_order_id(order_id: str) -> dict:
    """
    Retrieve a follow-up entry by its order_id.
    Args:
        order_id (str): The unique identifier for the order.
    Returns:
        dict: The follow-up entry if found, else an empty dict.
    """
    for entry in order_followup_data:
        if entry["order_id"] == order_id:
            return entry
    return {}

@function_tool
def search_followups_by_keyword(keyword: str) -> list:
    """
    Search for follow-up entries by (partial) keyword match in followup text (case-insensitive).
    Args:
        keyword (str): The (partial) keyword to search for.
    Returns:
        list: List of matching follow-up entries.
    """
    return [f for f in order_followup_data if keyword.lower() in f["followup"].lower()]

@function_tool
def list_all_followups() -> list:
    """
    List all available order follow-up entries.
    Returns:
        list: All follow-up entries in the database.
    """
    return order_followup_data
