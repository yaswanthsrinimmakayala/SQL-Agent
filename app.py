import streamlit as st
import sqlite3
import uuid
from model import answer
from tools import refresh
from data import actual_data

st.set_page_config(layout="wide", page_title="SQL Agent")

conn = sqlite3.connect("mydb.db")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

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
                response = answer(user_question, st.session_state.conversation_id)
            st.write(response)

    st.session_state.messages.append({"role": "assistant", "content": response})