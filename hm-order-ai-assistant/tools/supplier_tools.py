from agents import function_tool
from data.supplier_data import suppliers

@function_tool
def get_supplier_by_id(supplier_id: str) -> dict:
    """
    Retrieve a supplier by its unique supplier_id.
    Args:
        supplier_id (str): The unique identifier for the supplier.
    Returns:
        dict: The supplier data if found, else an empty dict.
    """
    for supplier in suppliers:
        if supplier["supplier_id"] == supplier_id:
            return supplier
    return {}

@function_tool
def search_suppliers_by_name(name: str) -> list:
    """
    Search for suppliers by (partial) name match (case-insensitive).
    Args:
        name (str): The (partial) name to search for.
    Returns:
        list: List of matching suppliers.
    """
    return [s for s in suppliers if name.lower() in s["name"].lower()]

@function_tool
def filter_suppliers(country: str = None, city: str = None, product_category: str = None) -> list:
    """
    Filter suppliers by country, city, and/or product_category. All filters are optional and case-insensitive.
    Args:
        country (str, optional): Filter by country.
        city (str, optional): Filter by city.
        product_category (str, optional): Filter by product category.
    Returns:
        list: List of suppliers matching all provided filters.
    """
    results = suppliers
    if country:
        results = [s for s in results if s["country"].lower() == country.lower()]
    if city:
        results = [s for s in results if s["city"].lower() == city.lower()]
    if product_category:
        results = [s for s in results if s["product_category"].lower() == product_category.lower()]
    return results

@function_tool
def list_all_suppliers() -> list:
    """
    List all available suppliers.
    Returns:
        list: All suppliers in the database.
    """
    return suppliers