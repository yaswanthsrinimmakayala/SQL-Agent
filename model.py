# initialization of model 
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from tools import RuntimeContext,execute_sql,db
from dotenv import load_dotenv
from langchain_core.messages import AIMessage
import os
load_dotenv()

model = init_chat_model(
    model = "gemini-2.5-flash",
    model_provider = "google_genai",
    temperature = 0,
    api_key = os.getenv("API_Key") 
)
prompt = """
You are an helful SQL agent.
Database schema:
- customers(id, name, email, city)
- categories(id, name)
- products(id, name, category_id, price)
- orders(id, customer_id, order_date, status, payment_method)
- order_items(id, order_id, product_id, quantity)
Rules:
- You will help the user by taking the user input, and will create SQL queries to relate the user input to answer them.
- You also follow actions specified by user such as modifications to the data as specified by user.
- Use the tools to perform actions.  
- Limit to 5 rows of output values unless explicitly asked.
- If the tool returns 'Error: ' , revise the SQL and try_again.
- Prefer explicit column lists; avoid select *.
- Always present query results as a clean markdown table, never as raw tuples or lists.
"""
agent = create_agent(
    model = model,
    tools = [execute_sql],
    system_prompt = prompt,
    context_schema = RuntimeContext
)
def extract_content(content):
    if isinstance(content, str):
        return content
    response = ""
    for indx in content:
        if indx["type"]=="text":
            response+=indx["text"]
            response+="\n"
    return response

def answer(question:str, thread_id:str)->str:
    result_stream = agent.stream(
        {"messages":[{"role":"user","content":question}]},
        config = {"configurable":{"thread_id":thread_id}},
        context = RuntimeContext(db=db),
        stream_mode = "values"
        )
    
    last_step = ""
    for step in result_stream:
        print(step)
        last_step = step
    
    for msg in reversed(last_step["messages"]):
        if isinstance(msg,AIMessage):
            return extract_content(msg.content)
    
    return "No response generated"

