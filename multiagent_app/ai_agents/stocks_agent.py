from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from tools import stocks_tools
import os
from openai import AsyncAzureOpenAI

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)


stocks_agent = Agent(
    name="StocksAgent",
    instructions=(
        "You are StocksAgent. Provide users with current stock data and simple analysis using your available tools. "
        "Clearly state that you do not provide investment advice or personalized financial recommendations. "
        "If a request is unclear or outside your scope, ask for clarification or suggest consulting a financial professional."
    ),
    tools=[stocks_tools.get_stock_quote, stocks_tools.run_simple_strategy],
    model=model
)
