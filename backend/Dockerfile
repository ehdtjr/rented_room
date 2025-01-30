FROM python:3.11

WORKDIR /backend

RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

COPY ./pyproject.toml ./poetry.lock* /backend/

RUN poetry install --only main --no-root

ENV PYTHONPATH=/backend

COPY . /backend

CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]