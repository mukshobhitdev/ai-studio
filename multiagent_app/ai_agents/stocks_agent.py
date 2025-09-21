from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from tools import stocks_tools
import os
from openai import AsyncAzureOpenAI

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

instructions=(
    "You are StocksAgent. Provide users with current stock data and simple analysis "
    "using your available tools. When returning results, strip suffixes like '.NS' or '.BO' "
    "and only display the base ticker (e.g., show 'TCS' instead of 'TCS.NS'). "
    "Clearly state that you do not provide investment advice or personalized financial recommendations. "
    "If a request is unclear or outside your scope, ask for clarification or suggest consulting a financial professional."
)

stocks_agent = Agent(
    name="StocksAgent",
    instructions=instructions,
    tools=[stocks_tools.get_stock_quote, stocks_tools.run_simple_strategy, stocks_tools.list_all_stocks],
    model=model
)
