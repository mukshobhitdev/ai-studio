from agents import function_tool

from data.stock_data import SAMPLE_STOCKS

@function_tool
def get_stock_quote(ticker: str) -> dict:
    """Return information for matching ticker.

    Args:
        ticker: The stock ticker symbol. 
    """ 
    info = SAMPLE_STOCKS.get(ticker.upper())
    if not info:
        return {"ticker": ticker, "error": "Ticker information is not available."}
    return {"ticker": ticker.upper(), "quote": info}

@function_tool
def run_simple_strategy(ticker: str, days: int = 30) -> dict:
    return {"ticker": ticker.upper(), "days": days, "performance": f"{round(0.02 * days, 2)}% (demo)"}

@function_tool
def list_all_stocks() -> list:
    """List all stocks in the sample data.
    """
    return [{"ticker": ticker, "info": info} for ticker, info in SAMPLE_STOCKS.items()]