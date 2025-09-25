from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from tools import supplier_tools
import os
from openai import AsyncAzureOpenAI

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

supplier_agent = Agent(
    name="SupplierAgent",
    instructions=(
        "You are SupplierAgent. Assist users in searching, filtering, and retrieving supplier information using your available tools. "
        "Ask clarifying questions about supplier details, location, or product category to provide the best results. "
        "If the request is unclear or outside your scope, ask for more details or suggest consulting a human expert."
    ),
    tools=[
        supplier_tools.get_supplier_by_id,
        supplier_tools.search_suppliers_by_name,
        supplier_tools.filter_suppliers,
        supplier_tools.list_all_suppliers
    ],
    model=model
)
