import streamlit as st
import sqlite3
import uuid
from model import answer
from tools import refresh
st.set_page_config(layout="wide")
conn = sqlite3.connect("mydb.db")
st.title("SQL Agent")

# Session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())


# Split screen
col1, col2 = st.columns([1, 1])  

with col1:
    st.subheader("💬 Chat")

    chat_container = st.container(height=500)
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])


    user_question = st.chat_input("Ask about the data")

    if user_question:
        st.session_state.messages.append({
            "role": "user",
            "content": user_question
        })
        response = answer(user_question, st.session_state.conversation_id)
        st.session_state.messages.append({
            "role": "assistant",
            "content": response
        })
 

with col2:
    st.subheader("📊 Data")
    refresh(conn)

