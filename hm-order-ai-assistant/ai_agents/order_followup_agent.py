import os
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from tools import knowledge_tools, order_followup_tools

load_dotenv(override=True)


DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

order_followup_agent = Agent(
    name="OrderFollowupAgent",
    instructions=(
        "You are OrderFollowupAgent. Assist users in searching, filtering, and retrieving order follow-up information using your available tools. "
        "Ask clarifying questions about order IDs, follow-up details, or preferences to provide the best results. "
        "If the request is unclear or outside your scope, ask for more details or suggest consulting a human expert."
    ),
    tools=[
        order_followup_tools.get_followup_by_order_id,
        order_followup_tools.search_followups_by_keyword,
        order_followup_tools.list_all_followups
    ],
    model=model
)
