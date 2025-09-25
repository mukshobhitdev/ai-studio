import os
from agents import Agent, OpenAIChatCompletionsModel
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from tools import article_tools

load_dotenv(override=True)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
client = AsyncAzureOpenAI()
model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

article_agent = Agent(
    name="ArticleAgent",
    instructions=(
        "You are ArticleAgent. Assist users in searching, filtering, and retrieving article information using your available tools. "
        "Ask clarifying questions about article details, categories, or preferences to provide the best results. "
        "If the request is unclear or outside your scope, ask for more details or suggest consulting a human expert."
    ),
    tools=[
        article_tools.get_article_by_id,
        article_tools.search_articles_by_name,
        article_tools.filter_articles,
        article_tools.list_all_articles,
        article_tools.get_article_price
    ],
    model=model
)