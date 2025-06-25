# Use slim Python 3.10 base image
FROM python:3.10-slim

# Set working directory inside the container
WORKDIR /app

# Copy all project files to the container
COPY . .

# Upgrade pip and install all dependencies from requirements.txt
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Start the app with uvicorn on port 10000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
