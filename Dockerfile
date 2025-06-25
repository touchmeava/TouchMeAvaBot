FROM python:3.10-slim

WORKDIR /app
COPY . .

# Install dependencies manually to ensure clean install
RUN pip install --upgrade pip && \
    pip uninstall -y aiogram && \
    pip install --no-cache-dir aiogram==3.3.0 fastapi uvicorn

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
