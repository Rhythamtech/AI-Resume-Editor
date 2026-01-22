import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()


def create_llm(temperature: float = 0.7):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key: 
        raise ValueError("OPENAI_API_KEY must be set when using OpenAI provider")
    
    model = os.getenv("OPENAI_MODEL")
    base_url = os.getenv("OPENAI_BASE_URL")
    
    kwargs = {
        "model": model,
        "temperature": temperature,
        "api_key": api_key
    }
    
    if base_url:
        kwargs["base_url"] = base_url
    
    return ChatOpenAI(**kwargs)
