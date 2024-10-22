import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Finsafe Q&A API"
    PROJECT_VERSION: str = "1.0.0"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    HF_TOKEN: str = os.getenv("HF_TOKEN")
    MONGO_URI: str = os.getenv("MONGO_URI")
    PERSIST_DIRECTORY: str = os.getenv("PERSIST_DIRECTORY")

settings = Settings()