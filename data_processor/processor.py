import re
import csv
import os

# 필드 추출 정규식
field_patterns = {
    "name": r"\n([^\n]+)\n*(도로명 주소)",  # 자취방 이름 필드 매칭
    "address": r"도로명 주소:\s*(.+?)\n",  # 도로명 주소 필드 매칭
    "contact": r"연락처\s*:\s*(.+?)\n",  # 연락처 필드 매칭
    "price": r"가격:\s*(.+?)\n",  # 가격 필드 매칭
    "fee": r"관리비/보증금:\s*([^\n]*)",  # 관리비/보증금 필드 매칭
    "options": r"옵션:\s*(.*?)\n",  # 옵션 필드 매칭
    "gas_type": r"LPG/심야전기/도시가스:\s*(.+?)\n",  # 가스 유형 필드 매칭
    "comment": r"\* (.+?)\n*제40대 총학생회",  # 비고 필드 매칭
}
# 위치 종류
place_type = {
    "back_gate": "후문",
    "main_gate": "정문",
    "middle_gate": "중문",
    "dormitory": "기숙사",
    "education_culture_center": "교육문화회관",
    "farming_mart": "농가마트",
}


class DataProcessor:
    def __init__(self, markdown_content):
        self.content = markdown_content

    # JSON에서 값 추출
    def export_json(self, place):
        entries = []

        # 자취방 이름(field_patterns["name"]) 기준으로 데이터 블록 추출
        block_starts = [
            m.start() for m in re.finditer(field_patterns["name"], self.content, re.M)
        ]
        block_starts.append(len(self.content))  # 마지막 끝 위치 추가

        for i in range(len(block_starts) - 1):
            entry_start = block_starts[i]
            entry_end = block_starts[i + 1]

            entry_text = self.content[entry_start:entry_end]

            # 각 필드 추출
            entry = {}
            for field, pattern in field_patterns.items():
                field_match = re.search(pattern, entry_text, re.S)
                entry[field] = field_match.group(1).strip() if field_match else "null"

            entry["place"] = place_type[place]

            entries.append(entry)

        return entries

    def json_to_csv(self, json_data):
        # CSV 파일 저장 경로 지정
        output_dir = "../data/csv_data"
        os.makedirs(output_dir, exist_ok=True)  # 디렉토리가 없으면 생성
        csv_file = os.path.join(output_dir, "rental_data.csv")

        # CSV 파일 저장
        fieldnames = [
            "name",
            "address",
            "contact",
            "price",
            "fee",
            "options",
            "gas_type",
            "comment",
            "place",
        ]

        with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(json_data)

        print(f"Data saved to {csv_file}")
