from data.travel_data import hotels, flights
from agents import function_tool

@function_tool
def search_flights(origin: str, dest: str, date: str) -> dict:
    """Search flights for given origin, destination and date. Return flights information.

    Args:
        origin: The starting location of the flight.
        dest: The destination location of the flight.
        date: The date of the flight.
    """
    return {"origin": origin, "destination": dest, "date": date, "flights": flights}

@function_tool
def book_flight(origin: str, dest: str, date: str) -> str:
    """Book a flight given the origin, destination, and date and Return the booking details including refernce number.

    Args:
        origin: The starting location of the flight.
        dest: The destination location of the flight.
        date: The date of the flight.
    """
    return f"Flight from {origin} to {dest} on {date} is booked. Reference number: FL123456"

@function_tool
def search_hotels(dest: str, checkin: str, nights: int = 2) -> dict:
    """search hotels for given destination, check-in date, and number of nights. Return the hotels bases on match.

    Args:
        dest: The destination location of the hotel.
        checkin: The check-in date for the hotel.
        nights: The number of nights to stay.
    """
    return {"destination": dest, "checkin": checkin, "nights": nights, "hotels": hotels}


@function_tool
def book_hotel(dest: str, checkin: str, nights: int = 2) -> str:
    """Book a hotel given the destination, check-in date, and number of nights. Return the booking details including reference number.

    Args:
        dest: The destination location of the hotel.
        checkin: The check-in date for the hotel.
        nights: The number of nights to stay.
    """
    return f"Hotel in {dest} booked from {checkin} for {nights} nights. Reference number: HT789012"
