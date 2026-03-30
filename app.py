# UI
import streamlit as st
import uuid
from model import answer
# Title
st.title("SQL Agent")
# Creation of session variable messages to store the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = ""

# Displaying the messages in the UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
user_question = st.chat_input("Ask about the data")
conv_id = uuid.uuid1()
# Writing the user input to UI and appending it to conversation (messages)
if user_question:
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role":"user","content":user_question})
    response = answer(user_question,conv_id)
    if response:
        with st.chat_message("assistant"):
            st.write(response)
            st.session_state.messages.append({"role":"assistant","content":response})
            