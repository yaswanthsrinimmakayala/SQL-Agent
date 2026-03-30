# UI
import streamlit as st
# Title
st.title("SQL Agent")
# Creation of session variable messages to store the conversation
if "messages" not in st.session_state:
    st.session_state.messages = []
# Displaying the messages in the UI
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User Input
user_question = st.chat_input("Ask about the data")

# Writing the user input to UI and appending it to conversation (messages)
if user_question:
    with st.chat_message("user"):
        st.write(user_question)
    st.session_state.messages.append({"role":"user","content":user_question})