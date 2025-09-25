
from agents import function_tool
from data.article_data import article_data


@function_tool
def get_article_by_id(article_id: str) -> dict:
    """
    Retrieve an article by its unique article_id.
    Args:
        article_id (str): The unique identifier for the article.
    Returns:
        dict: The article data if found, else an empty dict.
    """
    for article in article_data:
        if article["article_id"] == article_id:
            return article
    return {}

@function_tool
def search_articles_by_name(name: str) -> list:
    """
    Search for articles by (partial) name match (case-insensitive).
    Args:
        name (str): The (partial) name to search for.
    Returns:
        list: List of matching articles.
    """
    return [a for a in article_data if name.lower() in a["name"].lower()]

@function_tool
def filter_articles(category: str = None, type: str = None, color: str = None, size: str = None) -> list:
    """
    Filter articles by category, type, color, and/or size. All filters are optional and case-insensitive.
    Args:
        category (str, optional): Filter by category (e.g., 'Men', 'Women', 'Kids').
        type (str, optional): Filter by type (e.g., 'Jeans', 'Dress').
        color (str, optional): Filter by color (e.g., 'Blue').
        size (str, optional): Filter by size (e.g., 'M', '32').
    Returns:
        list: List of articles matching all provided filters.
    """
    results = article_data
    if category:
        results = [a for a in results if a["category"].lower() == category.lower()]
    if type:
        results = [a for a in results if a["type"].lower() == type.lower()]
    if color:
        results = [a for a in results if a["color"].lower() == color.lower()]
    if size:
        results = [a for a in results if a["size"].lower() == size.lower()]
    return results

@function_tool
def list_all_articles() -> list:
    """
    List all available articles.
    Returns:
        list: All articles in the database.
    """
    return article_data

@function_tool
def get_article_price(article_id: str) -> float:
    """
    Get the price of an article by its article_id.
    Args:
        article_id (str): The unique identifier for the article.
    Returns:
        float: The price of the article, or -1 if not found.
    """
    for article in article_data:
        if article["article_id"] == article_id:
            return article["price"]
    return -1.0