import os
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from tools import hm_order_tools

load_dotenv(override=True)


DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

hm_order_agent = Agent(
    name="HMOrderAgent",
    instructions=(
        "You are HMOrderAgent. Assist users in searching, filtering, and retrieving H&M order information using your available tools. "
        "Ask clarifying questions about order details, product, supplier, or status to provide the best results. "
        "If the request is unclear or outside your scope, ask for more details or suggest consulting a human expert."
    ),
    tools=[
        hm_order_tools.get_order_by_id,
        hm_order_tools.search_orders_by_product,
        hm_order_tools.filter_orders,
        hm_order_tools.list_all_orders,
        hm_order_tools.get_order_status,
        hm_order_tools.get_orders_by_supplier,
        hm_order_tools.get_orders_by_article_id
    ],
    model=model
)
