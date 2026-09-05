# CropGuard AI Production Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python requirements
COPY Backend/requirements.txt /app/Backend/requirements.txt
RUN pip install --no-cache-dir -r /app/Backend/requirements.txt

# Copy application code and datasets
COPY Backend /app/Backend
COPY Data /app/Data
COPY Practical_05_Reasoning /app/Practical_05_Reasoning
COPY Practical_09_NLP_App /app/Practical_09_NLP_App

EXPOSE 8000

CMD ["uvicorn", "Backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
