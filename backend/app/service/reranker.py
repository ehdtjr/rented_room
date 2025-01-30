# app/services/compression.py
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

# def get_compression_retriever(base_retriever, top_n: int = 4):
#     # 모델 초기화
#     model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")
#     compressor = CrossEncoderReranker(model=model, top_n=top_n)

#     compression_retriever = ContextualCompressionRetriever(
#         base_compressor=compressor, base_retriever=base_retriever
#     )
#     return compression_retriever


def get_crossencoder_reranker(top_n: int = 4):
    """
    검색된 문서 리스트에 대해, 별도 추가 검색 없이
    CrossEncoder로만 재랭크를 수행하기 위한 Reranker 생성 함수
    """
    # 1) 모델 초기화
    model = HuggingFaceCrossEncoder(model_name="BAAI/bge-reranker-v2-m3")

    # 2) CrossEncoderReranker 생성
    reranker = CrossEncoderReranker(model=model, top_n=top_n)
    return reranker
