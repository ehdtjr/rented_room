# app/services/vectorstore.py
from langchain_chroma import Chroma
from langchain_openai.embeddings import OpenAIEmbeddings
from app.core.config import settings

def get_vectorstore() -> Chroma:
    """Chroma VectorStore 인스턴스를 생성/반환합니다."""
    embeddings = OpenAIEmbeddings(model=settings.EMBEDDING_MODEL)
    persist_db = Chroma(
        persist_directory=settings.DB_PATH,
        embedding_function=embeddings,
        collection_name="rental_data_with_nan",  # 예시
    )
    return persist_db
