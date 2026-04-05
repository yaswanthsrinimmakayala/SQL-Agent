# initialization of model 
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from tools import RuntimeContext,execute_sql,db,get_tables,get_schema
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage,ToolMessage
import streamlit as st
import os
import json
load_dotenv()


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
def extract_content(content):
    if isinstance(content, str):
        return content
    response = ""
    for indx in content:
        if indx["type"]=="text":
            response+=indx["text"]
            response+="\n"
    return response

def answer(question:str, thread_id:str,agent)->str:
    result_stream = agent.stream(
        {"messages":[{"role":"user","content":question}]},
        config = {"configurable":{"thread_id":thread_id}},
        context = RuntimeContext(db=db),
        stream_mode = "values"
        )
    
    last_step = ""
    steps_executed = "These are steps followed:\n"
    for step in result_stream:
        print(json.dumps(step,indent=2, default=str))
        last_step = step
    
    for msg in last_step["messages"]:
        if isinstance(msg,AIMessage) and msg.tool_calls:
            schema_tables = []
            for tool_call in msg.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                if tool_name=="execute_sql":
                    steps_executed+=f"\nExecuting query{tool_args['query']}...\n"
                elif tool_name == "get_tables":
                    steps_executed += f"\nGetting the tables in the database\n"
                elif tool_name == "get_schema":
                    schema_tables.append(tool_args['table_name'])
            if schema_tables:
                steps_executed += f"\nInspecting schema of {', '.join(schema_tables)}\n"



    for msg in reversed(last_step["messages"]):
        if isinstance(msg,AIMessage):
            return steps_executed,extract_content(msg.content)
    
    return "No response generated"

