import os
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from tools import travel_tools

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

travel_agent = Agent(
    name="TravelAgent",
    instructions=(
        "You are TravelAgent. Assist users in planning travel by searching for flights and hotels and booking flights using your available tools. "
        "Ask clarifying questions about travel dates, destinations, preferences, and constraints to provide the best options. "
        "If the request is unclear or outside your scope, ask for more details or suggest consulting a travel professional."
    ),
    tools=[travel_tools.search_flights, travel_tools.book_flight, travel_tools.list_all_flights,
           travel_tools.book_hotel, travel_tools.search_hotels, travel_tools.list_all_hotels],
    model=model
)
