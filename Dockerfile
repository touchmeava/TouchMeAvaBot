FROM python:3.10-slim

WORKDIR /app
COPY . .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir fastapi uvicorn aiogram==3.3.0

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
