# app/services/retriever.py
from langchain.chains.query_constructor.base import (
    AttributeInfo,
    Comparison,
    Comparator,
    Operation,
    StructuredQuery,
)
from langchain.chains.query_constructor.base import (
    StructuredQueryOutputParser,
    get_query_constructor_prompt,
)
from langchain_openai import ChatOpenAI

from langchain.schema.runnable import Runnable
from langchain.retrievers.self_query.base import SelfQueryRetriever
from langchain.retrievers.self_query.chroma import ChromaTranslator

from app.service.vectorstore import get_vectorstore
from app.core.config import settings

# 1) 메타데이터 필드 정보 정의
metadata_field_info = [
    AttributeInfo(
        name="place",
        description="The location information of the rental room. One of ['정문', '중문', '후문', '기숙사', '농가마트', '교육문화회관']",
        type="string",
    ),
    AttributeInfo(
        name="oneroom_year",
        description="The annual rent price for a one-room unit.",
        type="float",
    ),
    AttributeInfo(
        name="oneroom_half_year",
        description="The half-year rent price for a one-room unit.",
        type="float",
    ),
    AttributeInfo(
        name="tworoom_half_year",
        description="The half-year rent price for a two-room unit.",
        type="float",
    ),
    AttributeInfo(
        name="tworoom_year",
        description="The annual rent price for a two-room unit.",
        type="float",
    ),
]


# 2) contain -> eq 변환 로직 (필터링)
def replace_contain_with_eq(filter):
    if isinstance(filter, Comparison):
        if filter.comparator == Comparator.CONTAIN:
            return Comparison(
                comparator=Comparator.EQ, attribute=filter.attribute, value=filter.value
            )
        elif filter.comparator == Comparator.LIKE:
            return Comparison(
                comparator=Comparator.EQ,
                attribute=filter.attribute,
                value=filter.value.replace("%", ""),
            )
        return filter
    elif isinstance(filter, Operation):
        return Operation(
            operator=filter.operator,
            arguments=[replace_contain_with_eq(arg) for arg in filter.arguments],
        )
    return filter


def preprocess_and_wrap_structured_query(query: StructuredQuery) -> StructuredQuery:
    if query.filter:
        transformed_filter = replace_contain_with_eq(query.filter)
    else:
        transformed_filter = None

    return StructuredQuery(
        query=query.query, filter=transformed_filter, limit=query.limit
    )


# Runnable
class FilterTransformRunnable(Runnable):
    def invoke(self, structured_query: StructuredQuery, config=None) -> StructuredQuery:
        return preprocess_and_wrap_structured_query(structured_query)


filter_transform = FilterTransformRunnable()

# 3) StructuredQueryOutputParser 생성
output_parser = StructuredQueryOutputParser.from_components()

# 4) LLM 초기화
llm = ChatOpenAI(
    temperature=0, model="gpt-4o", openai_api_key=settings.OPENAI_API_KEY  # 사용 모델
)

# 5) query_constructor prompt
prompt_template = get_query_constructor_prompt(
    "Brief summary of a rental room",  # 문서 내용
    metadata_field_info,  # 메타데이터 필드
)

# 6) chain
query_constructor = prompt_template | llm | output_parser | filter_transform


def get_self_query_retriever():
    vectorstore = get_vectorstore()
    retriever = SelfQueryRetriever(
        query_constructor=query_constructor,
        vectorstore=vectorstore,
        structured_query_translator=ChromaTranslator(),
        search_kwargs={"k": 10},
    )
    return retriever
