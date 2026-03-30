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
prompt = ''
agent = create_agent(
    model = model,
    tools = [],
    system_prompt = prompt
)
