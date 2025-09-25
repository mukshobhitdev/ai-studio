from agents import function_tool
from data.hm_order_data import hm_order_data

@function_tool
def get_order_by_id(order_id: str) -> dict:
    """
    Retrieve an order by its unique order_id.
    Args:
        order_id (str): The unique identifier for the order.
    Returns:
        dict: The order data if found, else an empty dict.
    """
    for order in hm_order_data:
        if order["order_id"] == order_id:
            return order
    return {}

@function_tool
def search_orders_by_product(product: str) -> list:
    """
    Search for orders by (partial) product name match (case-insensitive).
    Args:
        product (str): The (partial) product name to search for.
    Returns:
        list: List of matching orders.
    """
    return [o for o in hm_order_data if product.lower() in o["product"].lower()]

@function_tool
def get_orders_by_supplier(supplier_id: str) -> list:
    """
    Retrieve all orders from a specific supplier by supplier_id.
    Args:
        supplier_id (str): The unique identifier for the supplier.
    Returns:
        list: List of orders from the specified supplier.
    """
    return [order for order in hm_order_data if order["supplier_id"].lower() == supplier_id.lower()]

@function_tool  
def get_orders_by_article_id(article_id: str) -> list:
    """
    Retrieve all orders containing a specific article by article_id.
    Args:
        article_id (str): The unique identifier for the article.
    Returns:
        list: List of orders containing the specified article.
    """
    return [order for order in hm_order_data if article_id == order.get("article_id")]

@function_tool  
def get_orders_by_article_id(article_id: str) -> list:
    """
    Retrieve all orders containing a specific article by article_id.
    Args:
        article_id (str): The unique identifier for the article.
    Returns:
        list: List of orders containing the specified article.
    """
    return [order for order in hm_order_data if article_id == order.get("article_id")]


@function_tool
def filter_orders(status: str = None, supplier_id: str = None, order_date: str = None, delivery_date: str = None) -> list:
    """
    Filter orders by status, supplier_id, order_date, and/or delivery_date. All filters are optional and case-insensitive.
    Args:
        status (str, optional): Filter by order status (e.g., 'Shipped', 'Processing', 'Confirmed').
        supplier_id (str, optional): Filter by supplier ID.
        order_date (str, optional): Filter by order date (YYYY-MM-DD).
        delivery_date (str, optional): Filter by delivery date (YYYY-MM-DD).
    Returns:
        list: List of orders matching all provided filters.
    """
    results = hm_order_data
    if status:
        results = [o for o in results if o["status"].lower() == status.lower()]
    if supplier_id:
        results = [o for o in results if o["supplier_id"].lower() == supplier_id.lower()]
    if order_date:
        results = [o for o in results if o["order_date"] == order_date]
    if delivery_date:
        results = [o for o in results if o["delivery_date"] == delivery_date]
    return results

@function_tool
def list_all_orders() -> list:
    """
    List all available orders.
    Returns:
        list: All orders in the database.
    """
    return hm_order_data

@function_tool
def get_order_status(order_id: str) -> str:
    """
    Get the status of an order by its order_id.
    Args:
        order_id (str): The unique identifier for the order.
    Returns:
        str: The status of the order, or 'Not found' if not found.
    """
    for order in hm_order_data:
        if order["order_id"] == order_id:
            return order["status"]
    return "Not found"