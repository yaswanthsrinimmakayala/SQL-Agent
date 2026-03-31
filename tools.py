from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from langchain_community.utilities import SQLDatabase
from dataclasses import dataclass
import streamlit as st

db = SQLDatabase.from_uri("sqlite:///mydb.db")

@dataclass
class RuntimeContext:
    db : SQLDatabase

@tool 
def execute_sql(query:str)->str:
    """Execute a SQLite command and return results"""
    runtime = get_runtime(RuntimeContext)
    db = runtime.context.db
    try:
        return db.run(query)
    except Exception as e:
        return f"Error: {e}"
    

def refresh(conn):
    st.write(conn.execute("SELECT *FROM CUSTOMERS"))
    st.write(conn.execute("SELECT *FROM ORDERS"))
    st.write(conn.execute("SELECT *FROM CATEGORIES"))
    st.write(conn.execute("SELECT *FROM PRODUCTS"))
    
