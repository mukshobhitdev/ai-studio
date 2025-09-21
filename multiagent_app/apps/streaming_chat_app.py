
import asyncio
import streamlit as st
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel 
from openai import AsyncAzureOpenAI
import sys
import os

# Add the parent directory to the path so we can import the agents module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agents import doc_agent, medical_agent, research_agent, stocks_agent, travel_agent
from tools  import memory_tools

# Add the parent directory to the path so we can import the agents module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Multi Agent System",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Multi Agent System")

with st.sidebar:
    st.header("Configuration")
    agent_name = st.text_input("Agent Name", "Lead Agent")
    
    systemMessage=(
        "You are LeadAgent. Always greet the user by their name if it is available in memory, otherwise ask for their name. "
        "Your job is to triage user queries and hand off to one of the available specialist agents: ResearchAgent, DocAgent, MedicalAgent, StocksAgent, or TravelAgent. "
        "If the query is unclear, ask clarifying questions to determine the correct agent. "
        "Never provide general information, facts, or answers yourself. Do not answer questions outside the scope of the available agents. "
    )
    agent_instructions = st.text_area("Agent Instructions", systemMessage, height=450)
    
    st.markdown("---")


# User input area (submit on Enter)
user_input = st.text_input("Message:", value="Hello")
send_button = st.button("Send", type="primary")

# Response area with custom styling
response_container = st.container()

session = SQLiteSession("conversation_1", "conversations.db")

async def stream_response(agent: Agent, user_input: str) -> None:
    """Stream agent response and update the UI."""
    response_parts = ""
    try:
        result = Runner.run_streamed(agent, input=user_input,session=session, max_turns=6)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                response_parts += event.data.delta
                message_placeholder.markdown(response_parts + "▌")
        message_placeholder.markdown(response_parts)
    except Exception as e:
        st.error(f"An error occurred: {e}")

if send_button and user_input:
    DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    client = AsyncAzureOpenAI()
    model =OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)
    
    agent = Agent(
        name=agent_name,
        instructions=agent_instructions,
        handoffs=[research_agent, doc_agent, medical_agent, stocks_agent, travel_agent],
        tools=[memory_tools.save_memory, memory_tools.find_similar_memories, memory_tools.find_all_memories],
        model=model
    )
    
    with response_container:
        message_placeholder = st.empty()
        
        with st.spinner("Thinking..."):
            asyncio.run(stream_response(agent, user_input))

        if st.button("Clear"):
            st.experimental_rerun()

# Instructions
if not send_button:
    with response_container:
        st.info("👆 Enter your message above and click 'Send' to see the streaming response.")