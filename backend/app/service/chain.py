# app/services/chain.py

import os
from pathlib import Path

from service.retriever import get_self_query_retriever
from langchain_core.runnables import RunnablePassthrough
from langchain_core.prompts import load_prompt
from langchain.schema.runnable import RunnableMap, RunnableSequence
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from core.config import settings


def get_rag_chain(query : str):
    # 1) self query retriever
    retriever = get_self_query_retriever()

    # 2) 현재 파일( chain.py )을 기준으로 절대 경로 산출
    CURRENT_FILE = Path(__file__).resolve()  # chain.py의 절대 경로
    BASE_DIR = (
        CURRENT_FILE.parent.parent.parent
    )  # chain.py → service → app → (한 단계 위)
    PROMPTS_FILE = BASE_DIR / "prompts" / "rented_room.yaml"

    # 3) prompt 템플릿 로드 (절대 경로 사용)
    prompt_template = load_prompt(str(PROMPTS_FILE))

    # 4) LLM
    llm = ChatOpenAI(
        temperature=0, model="gpt-4o", openai_api_key=settings.OPENAI_API_KEY
    )

    # 5) Runnable 체인 정의
    chain = (
        {"context": {}, "question": RunnablePassthrough()}
        | prompt_template
        | llm
        | StrOutputParser()
    )
    return chain


def rag_pipeline(query: str) -> str:
    chain = get_rag_chain(query)
    # chain = get_self_query_retriever()
    answer = chain.invoke(query)
    return answer
