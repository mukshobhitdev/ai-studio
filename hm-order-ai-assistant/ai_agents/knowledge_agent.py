from agents import Agent,OpenAIChatCompletionsModel
from dotenv import load_dotenv
from tools import article_tools, knowledge_tools
import os
from openai import AsyncAzureOpenAI

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

knowledge_agent = Agent(
    name="KnowledgeAgent",
    instructions=(
        "You are KnowledgeAgent. Assist users in searching, filtering, and retrieving knowledge information using your available tools. "
        "Ask clarifying questions about knowledge topics, keywords, or preferences to provide the best results. "
        "If the request is unclear or outside your scope, ask for more details or suggest consulting a human expert."
    ),
    tools=[
        knowledge_tools.get_knowledge_by_topic,
        knowledge_tools.search_knowledge_by_keyword,
        knowledge_tools.list_all_knowledge
    ],
    model=model
)
