import asyncio
import streamlit as st
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncAzureOpenAI
import sys
import os

# Initialize chat history in session state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'pending_input' not in st.session_state:
    st.session_state['pending_input'] = None

# Add the parent directory to the path so we can import the agents module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ai_agents import doc_agent, medical_agent, research_agent, stocks_agent, travel_agent
from tools import memory_tools

agent_icon = "🤖"

# Streamlit page config
st.set_page_config(
    page_title="Multi Agent System",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Multi Agent System")

with st.sidebar:
    st.header("Configuration")
    agent_name = st.text_input("Agent Name", "Lead Agent")

    systemMessage = (
        "You are LeadAgent. Always greet the user by their name if it is available in memory, otherwise ask for their name. "
        "Your job is to triage user queries and hand off to one of the available specialist agents: ResearchAgent, DocAgent, MedicalAgent, StocksAgent, or TravelAgent. "
        "If the query is unclear, ask clarifying questions to determine the correct agent. "
        "Never provide general information, facts, or answers yourself. Do not answer questions outside the scope of the available agents. "
    )
    agent_instructions = st.text_area("Agent Instructions", systemMessage, height=450)

    st.markdown("---")

# Response area
response_container = st.container()

# Display chat history with alignment
# Display chat history with alignment
# Display chat history with alignment
with response_container:
    for entry in st.session_state['chat_history']:
        if entry['role'] == 'user':
            st.markdown(
                f"""
                <div style='display: flex; justify-content: flex-end;'>
                    <div style='background-color:#2f2f2f;
                                color:#ffffff;
                                border-radius:12px;
                                padding:8px 12px;
                                margin:4px 0;
                                display:inline-block;
                                max-width:70%;'>
                        <b>You:</b> {entry['content']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
           st.markdown(
                f"""
                <div style='display: flex; align-items: flex-start; margin:4px 0;'>
                    <div style='margin-right:8px; font-size:20px;'>{agent_icon}</div>
                    <div>{entry['content']}</div>
                </div>
                """,
                unsafe_allow_html=True,
           )


# Leave some margin before input panel
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])  # adjust ratio as needed
    with col1:
        user_input = st.text_input("Message:", "", key="user_message", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("Send", type="primary")


session = SQLiteSession("conversation_1", "conversations.db")


async def stream_response(agent: Agent, user_input: str) -> str:
    """Stream agent response and update UI live. Returns full response."""
    response_parts = ""
    try:
        result = Runner.run_streamed(agent, input=user_input, session=session, max_turns=6)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                response_parts += event.data.delta
                message_placeholder.markdown(
                    f"<div style='text-align: left; margin:4px 0;'>"
                    f"<div style='margin-right:8px; font-size:20px;'>{agent_icon}</div> {response_parts}▌</div>",
                    unsafe_allow_html=True,
                )
        # Final message (remove cursor)
        message_placeholder.markdown(
            f"<div style='text-align: left; margin:4px 0;'>"
            f"<div style='margin-right:8px; font-size:20px;'>{agent_icon}</div> {response_parts}</div>",
            unsafe_allow_html=True,
        )
        return response_parts
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""


# Step 1: Store user input immediately, then rerun to display it
if submitted and user_input.strip():
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    st.session_state['pending_input'] = user_input  # save for processing
    st.rerun()

# Step 2: After rerun, process pending input (agent response)
if st.session_state.get("pending_input"):
    DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    client = AsyncAzureOpenAI()
    model = OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

    agent = Agent(
        name=agent_name,
        instructions=agent_instructions,
        handoffs=[research_agent, doc_agent, medical_agent, stocks_agent, travel_agent],
        tools=[
            memory_tools.save_memory,
            memory_tools.find_similar_memories,
            memory_tools.find_all_memories,
        ],
        model=model,
    )

    with response_container:
        message_placeholder = st.empty()
        with st.spinner("Thinking..."):
            agent_response = asyncio.run(stream_response(agent, st.session_state["pending_input"]))
        st.session_state['chat_history'].append({"role": "agent", "content": agent_response})

    st.session_state['pending_input'] = None
    st.rerun()
