from agents import Agent,OpenAIChatCompletionsModel
from dotenv import load_dotenv
from tools import doc_tools, research_tools
import os
from openai import AsyncAzureOpenAI

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

doc_agent = Agent(
    name="DocAgent",
    instructions=(
        "You are DocAgent. Your role is to help users with document analysis tasks. "
        "You can extract entities, compare documents, and summarize text. "
        "Always provide clear, concise, and structured responses. "
        "If the user provides multiple documents, compare or summarize as requested. "
        "If the request is unclear, ask for clarification."
    ),
    tools=[doc_tools.extract_entities, doc_tools.compare_documents, research_tools.summarize_text],
    model=model
)
