from data.travel_data import hotels, flights
from agents import function_tool

@function_tool
def search_flights(origin: str, dest: str, date: str) -> dict:
    return {"origin": origin, "destination": dest, "date": date, "flights": flights}

@function_tool
def search_hotels(dest: str, checkin: str, nights: int = 2) -> dict:
    return {"destination": dest, "checkin": checkin, "nights": nights, "hotels": hotels}
