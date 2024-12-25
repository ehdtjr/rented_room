from typing import TypedDict, Annotated, List, Dict
import operator


class PdfState(TypedDict):
    startpage: Annotated[int, "startpage"]  # 시작 페이지
    endpage: Annotated[int, "endpage"]  # 끝 페이지
    filepath: Annotated[str, "filepath"]  # 원본 파일 경로
    split_pdf_data_list: Annotated[List[bytes], "split_pdf_data_list"]
    split_filepaths: Annotated[List[str], "split_filepaths"]
    ask_human: bool  # 사람에게 질문을 던질지 여부

