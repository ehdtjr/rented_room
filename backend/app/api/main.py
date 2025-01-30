from app.api.routes import chat
from fastapi import APIRouter
from starlette.middleware.cors import CORSMiddleware

api_router = APIRouter()

# 라우터 추가
api_router.include_router(chat.router, prefix="/rag", tags=["RAG"])