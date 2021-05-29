FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install --upgrade pip

COPY requirements.txt .

RUN pip install -r requirements.txt

EXPOSE 8000

WORKDIR /app/

COPY src/ src/

COPY alembic/ alembic/

COPY alembic.ini alembic.ini

COPY test/ test/