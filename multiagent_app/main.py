import os
from dotenv import load_dotenv
from openai.types.responses import ResponseTextDeltaEvent
from ai_agents import doc_agent, medical_agent, research_agent, stocks_agent, travel_agent

from tools  import memory_tools
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel 
from openai import AsyncAzureOpenAI
import logging
import asyncio
import nest_asyncio

load_dotenv(override=True)

logging.getLogger("openai").setLevel(logging.ERROR)

DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

client = AsyncAzureOpenAI()

model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

lead_agent = Agent(
    name="LeadAgent",
    instructions=(
        "You are LeadAgent. Always greet the user by their name if it is available in memory, otherwise ask for their name. "
        "Your job is to triage user queries and hand off to one of the available specialist agents: "
        "ResearchAgent, DocAgent, MedicalAgent, StocksAgent, or TravelAgent. "
        "You must NOT answer any user query directly, including common knowledge, general facts, or simple questions. "
        "ALWAYS hand off every user query to the most relevant specialist agent, even for basic or widely known information. "
        "If the query is unclear, ask clarifying questions to determine the correct agent. "
        "Never provide general information, facts, or answers yourself. Do not answer questions outside the scope of the available agents. "
    ),
    handoffs=[research_agent, doc_agent, medical_agent, stocks_agent, travel_agent],
    tools=[memory_tools.save_memory, memory_tools.find_similar_memories],
    model=model
)

session = SQLiteSession("conversation_1", "conversations.db")


async def main():
    GREEN = "\033[92m"  # Bright green
    RESET = "\033[0m"   # Reset to default color
    PINK = "\033[95m"  # Bright pink
    
    print(f"{PINK}\n=== Welcome to Agentic World ==={RESET}\n")
    
    while True:
        user_in = input("User: ").strip()
        
        if user_in.lower() in ("exit", "quit"):
            break
        elif user_in.lower() == "cls":
            os.system('cls' if os.name == 'nt' else 'clear')
            continue
                
        # result = await Runner.run_sync(lead_agent, user_in, session=session, max_turns=6)
        # print("Assistant:", result.final_output)
        
        result = Runner.run_streamed(lead_agent, user_in, session=session, max_turns=6)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                for char in event.data.delta:
                    print(f"{GREEN}{char}{RESET}", end="", flush=True)
                    await asyncio.sleep(0.02)  # Adjust delay for speed (0.02 = 20ms per char)
        
        print('\n')
        
nest_asyncio.apply()  

if __name__ == "__main__":
     asyncio.get_event_loop().run_until_complete(main())