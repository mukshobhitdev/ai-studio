import os
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from tools import research_tools

load_dotenv(override=True)


DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

research_agent = Agent(
    name="ResearchAgent",
    instructions=(
        "You are ResearchAgent. Assist users with research tasks by searching academic papers, summarizing content, and providing topic statistics. "
        "Use your tools to deliver accurate and concise information. "
        "If the user's request is unclear or too broad, ask clarifying questions to better understand their needs. "
        "Always cite sources or provide references when possible."
    ),
    tools=[research_tools.search_papers, research_tools.summarize_text, research_tools.fetch_statistics],
    model=model
)
