from dataclasses import dataclass
from dotenv import load_dotenv
import os
load_dotenv()
@dataclass
class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    LANGSMITH_API_KEY: str = os.getenv("LANGSMITH_API_KEY", "")
    FAISS_INDEX_PATH: str = os.getenv("FAISS_INDEX_PATH", "faiss_index.pkl")
    PERSIST_FAISS: bool = os.getenv("PERSIST_FAISS", "false").lower() in ("1","true","yes")

settings = Settings()
