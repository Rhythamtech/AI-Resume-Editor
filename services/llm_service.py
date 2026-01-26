from langchain_openai import ChatOpenAI
from config import settings


def create_llm(temperature: float = None):
    """
    Create and configure an LLM instance.
    
    Args:
        temperature: Temperature for the LLM. If None, uses default from settings.
        
    Returns:
        ChatOpenAI: Configured LLM instance.
        
    Raises:
        ValueError: If OPENAI_API_KEY is not set.
    """
    settings.validate()
    
    if temperature is None:
        temperature = settings.default_temperature
    
    kwargs = {
        "model": settings.openai_model,
        "temperature": temperature,
        "api_key": settings.openai_api_key
    }
    
    if settings.openai_base_url:
        kwargs["base_url"] = settings.openai_base_url
    
    return ChatOpenAI(**kwargs)
