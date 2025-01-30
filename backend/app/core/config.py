# app/core/config.py
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # .env 파일 로드


class Settings:
    # OpenAI API Key
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # 현재 파일 기준으로 절대 경로를 산출
    CURRENT_FILE = Path(__file__).resolve()  
    # 최상위 'backend' 폴더까지 이동
    BASE_DIR = CURRENT_FILE.parent.parent.parent
    # DB 경로를 절대 경로로 구성
    DB_PATH: str = str(BASE_DIR / "chroma_db")

    EMBEDDING_MODEL: str = "text-embedding-3-small"


settings = Settings()
