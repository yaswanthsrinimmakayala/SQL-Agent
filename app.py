import streamlit as st
import sqlite3
import uuid
from model import answer
from data import actual_data
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from tools import RuntimeContext,execute_sql,db,get_tables,get_schema
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
import streamlit as st
import os

st.set_page_config(layout="wide", page_title="SQL Agent")
def refresh(conn):
    st.write(conn.execute("SELECT *FROM CUSTOMERS"))
    st.write(conn.execute("SELECT *FROM ORDERS"))
    st.write(conn.execute("SELECT *FROM CATEGORIES"))
    st.write(conn.execute("SELECT *FROM PRODUCTS"))
conn = sqlite3.connect("mydb.db")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())
if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()
if "model" not in st.session_state:
    st.session_state.model  = init_chat_model(
    model = "gemini-2.5-flash",
    model_provider = "google_genai",
    temperature = 0,
    api_key = os.getenv("API_Key") 
)
prompt = """
You are an helful SQL agent.
Rules:
- You will help the user by taking the user input, and will create SQL queries to relate the user input to answer them.
- You also follow actions specified by user such as modifications to the data as specified by user.
- Use the tools to perform actions.  
- Limit to 5 rows of output values unless explicitly asked.
- If the tool returns 'Error: ' , revise the SQL and try_again.
- Prefer explicit column lists; avoid select *.
- Always present query results as a clean markdown table, never as raw tuples or lists.
"""
if "agent" not in st.session_state:
    st.session_state.agent = create_agent(
        model = st.session_state.model,
        tools = [execute_sql,get_schema,get_tables],
        system_prompt = prompt,
        context_schema = RuntimeContext,
        checkpointer = st.session_state.memory
    )

st.title("SQL Agent")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Chat")
    chat_container = st.container(height=600)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

with col2:
    st.subheader("📊 Data")
    if st.button("Actual Data"):
        actual_data()
        refresh(conn)
    with st.container(height=550):
        refresh(conn)

user_question = st.chat_input("Ask about the data...")

if user_question:
    st.session_state.messages.append({"role": "user", "content": user_question})

    with chat_container:
        with st.chat_message("user"):
            st.write(user_question)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    steps,response = answer(user_question, st.session_state.conversation_id,st.session_state.agent)
                    with st.expander("🔍 Steps Executed"):
                        st.write(steps)
                    st.write(response)
                except Exception as e:
                    response = "Hey Buddy, Time's up .Quota Reached!  "
                    st.write("Hey Buddy, Time's up .Quota Reached!  ",e) 

    st.session_state.messages.append({"role": "assistant", "content": response})