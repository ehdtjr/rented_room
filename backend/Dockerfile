FROM python:3.11

# (1) WORKDIR을 `/backend`로 설정하여 pyproject.toml을 찾을 수 있도록 함
WORKDIR /backend

# (2) Poetry 설치
RUN pip install --no-cache-dir poetry
RUN poetry config virtualenvs.create false

# (3) pyproject.toml과 poetry.lock 파일 복사
COPY ./pyproject.toml ./poetry.lock* /backend/

# (4) Poetry로 의존성 설치
RUN poetry install --only main --no-root

# (5) 전체 코드 복사
COPY . /backend

# (6) 환경 변수 설정
ENV PYTHONPATH=/backend

# (7) FastAPI 실행
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
