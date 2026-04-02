import streamlit as st
import sqlite3
import uuid
from model import answer
from tools import refresh
from data import actual_data

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
                    response = answer(user_question, st.session_state.conversation_id)
                    st.write(response)
                except Exception as e:
                    response = "Hey Buddy, Time's up .Quota Reached!  "
                    st.write("Hey Buddy, Time's up .Quota Reached!  ",e) 

    st.session_state.messages.append({"role": "assistant", "content": response})