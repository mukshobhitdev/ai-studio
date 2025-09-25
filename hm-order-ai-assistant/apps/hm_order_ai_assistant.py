import asyncio
import streamlit as st
from openai.types.responses import ResponseTextDeltaEvent
from agents import Agent, Runner, SQLiteSession, OpenAIChatCompletionsModel
from openai import AsyncAzureOpenAI
import sys
import os
import sqlite3
import logging


logging.getLogger("openai").setLevel(logging.ERROR)

# Load CSS
def load_css(file_name="chat_styles.css"):
    file_path = os.path.join(os.path.dirname(__file__), file_name)
    with open(file_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize chat state
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []
if 'pending_input' not in st.session_state:
    st.session_state['pending_input'] = None

# Add parent directory for custom modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ai_agents import article_agent, hm_order_agent, knowledge_agent, order_followup_agent, supplier_agent
from tools import memory_tools

# Page config
st.set_page_config(page_title="H&M Order AI Assistant", page_icon="🛒", layout="wide")
st.title("🛒 H&M Order AI Assistant")

# Sidebar
with st.sidebar:
    st.header("Configuration")
    agent_name = st.text_input("Agent Name", "H&M Order AI Assistant")

    systemMessage = (
        "You are the H&M Order AI Assistant. Greet the user by their name if available in memory, otherwise ask for their name. "
        "You help users track and manage H&M orders, suppliers, articles, and order follow-ups, and find relevant knowledge. "
        "Triage user queries and hand off to the appropriate specialist agent: ArticleAgent, HMOrderAgent, KnowledgeAgent, OrderFollowupAgent, or SupplierAgent. "
        "If the query is unclear, ask clarifying questions to determine the correct agent. "
        "Never provide general information, facts, or answers yourself. Do not answer questions outside the scope of the available agents. "
        "Always be helpful, concise, and focused on H&M order management."
    )
    agent_instructions = st.text_area("Agent Instructions", systemMessage, height=450)
    st.markdown("---")

    # Clear All Button
    if st.button("Clear All"):
        # Clear Streamlit session state
        st.session_state.clear()

        # Clear SQLite DB (delete all rows from user tables, do not drop sqlite_sequence)
        try:
            conn = sqlite3.connect("conversations.db")
            cursor = conn.cursor()
            # Get all user table names (exclude sqlite_sequence and other system tables)
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
            tables = cursor.fetchall()
            for table_name in tables:
                cursor.execute(f"DELETE FROM {table_name[0]};")
                # Optionally reset AUTOINCREMENT
                cursor.execute("DELETE FROM sqlite_sequence WHERE name=?;", (table_name[0],))
            conn.commit()
            conn.close()
            st.success("All conversations cleared!")
        except Exception as e:
            st.error(f"Failed to clear database: {e}")

        st.rerun()

# Response container
response_container = st.container()
agent_icon = "🤖"

# Display chat history
with response_container:
    for entry in st.session_state['chat_history']:
        if entry['role'] == 'user':
            st.markdown(
                f"""
                <div class="user-message-container">
                    <div class="user-message">{entry['content']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="agent-message-container">
                    <div class="agent-icon">{agent_icon}</div>
                    <div>{entry['content']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

# Margin above input panel
st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)

# Input form
with st.form(key="chat_form", clear_on_submit=True):
    col1, col2 = st.columns([9, 1])
    with col1:
        user_input = st.text_input("Message:", "", key="user_message", label_visibility="collapsed")
    with col2:
        submitted = st.form_submit_button("Send", type="primary")

# SQLite session
session = SQLiteSession("conversation_1", "conversations.db")

# Streamed agent response
async def stream_response(agent: Agent, user_input: str) -> str:
    response_parts = ""
    try:
        result = Runner.run_streamed(agent, input=user_input, session=session, max_turns=6)
        async for event in result.stream_events():
            if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
                response_parts += event.data.delta
                message_placeholder.markdown(
                    f"""
                    <div class="agent-message-container">
                        <div class="agent-icon">{agent_icon}</div>
                        <div>{response_parts}▌</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        # Final message
        message_placeholder.markdown(
            f"""
            <div class="agent-message-container">
                <div class="agent-icon">{agent_icon}</div>
                <div>{response_parts}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return response_parts
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return ""

# Step 1: Show user message immediately
if submitted and user_input.strip():
    st.session_state['chat_history'].append({"role": "user", "content": user_input})
    st.session_state['pending_input'] = user_input
    st.rerun()

# Step 2: Process agent response
if st.session_state.get("pending_input"):
    DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    client = AsyncAzureOpenAI()
    model = OpenAIChatCompletionsModel(model=DEPLOYMENT, openai_client=client)

    agent = Agent(
        name=agent_name,
        instructions=agent_instructions,
        handoffs=[article_agent, hm_order_agent, knowledge_agent, order_followup_agent, supplier_agent],
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
