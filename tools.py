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

@tool
def get_tables():
    """Use this tool to get the list of tables present in the database"""
    runtime = get_runtime(RuntimeContext)
    db = runtime.context.db
    try:
        return db.run("SELECT name FROM sqlite_master WHERE type='table'")
    except Exception as e:
        return f"Error :{e}" 
@tool
def get_schema(table_name:str)->str:
    """Use this tool to get the information about the schema information of a table in the database"""
    runtime = get_runtime(RuntimeContext)
    db = runtime.context.db
    try:
        return db.run(f"PRAGMA table_info({table_name})")
    except Exception as e:
        return f"Error : {e}"

    
