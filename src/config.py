import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # LLM Settings
    # Change "openai" to "groq" here to switch the whole system
    MODEL_PROVIDER = os.getenv("MODEL_PROVIDER", "openai") 
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    # Model Names
    OPENAI_MODEL = "gpt-4o-mini"
    GROQ_MODEL = "qwen/qwen3-32b"

    # SMTP Settings
    SMTP_HOST = os.getenv("SMTP_HOST", "localhost")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 1025))
    SENDER_EMAIL = "outreach@nexusai.com"