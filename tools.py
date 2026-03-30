from langchain_core.tools import tool
from langgraph.runtime import get_runtime
from langchain_community.utilities import SQLDatabase
from dataclasses import dataclass

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
    
