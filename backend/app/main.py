from fastapi import FastAPI
from app.api.main import api_router

app = FastAPI()

# Include RAG router
app.include_router(api_router, prefix="/api")
