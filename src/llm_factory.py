from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from src.config import Config

def get_llm(temperature=0):
    """
    Factory function to return an LLM instance based on the Config provider.
    """
    if Config.MODEL_PROVIDER == "openai":
        return ChatOpenAI(
            api_key=Config.OPENAI_API_KEY,
            model=Config.OPENAI_MODEL,
            temperature=temperature
        )
    elif Config.MODEL_PROVIDER == "groq":
        return ChatGroq(
            api_key=Config.GROQ_API_KEY,
            model=Config.GROQ_MODEL,
            temperature=temperature
        )
    else:
        raise ValueError(f"Unsupported provider: {Config.MODEL_PROVIDER}")