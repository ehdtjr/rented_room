# app/routers/rental_router.py
from fastapi import APIRouter, Query
from app.service.chain import rag_pipeline

router = APIRouter()


@router.get("/chat")
def chat_rented_room(query: str = Query(..., description="사용자 질문")):

    answer = rag_pipeline(query)
    return {"question": query, "answer": answer}
