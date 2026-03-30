# initialization of model 
from langchain.agent import create_agent
from langchain.chat_models import init_chat_model
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
Rules:
- You will help the user by taking the user input, and will create SQL queries to relate the user input to answer them.
- You also follow actions specified by user such as modifications to the data as specified by user.
- Use the tools to perform actions.  
- Limit to 5 rows of output values unless explicitly asked.
- If the tool returns 'Error: ' , revise the SQL and try_again.
- Prefer explicit column lists; avoid select *.
"""
agent = create_agent(
    model = model,
    tools = [],
    system_prompt = prompt
)
