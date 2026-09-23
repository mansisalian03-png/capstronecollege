FROM python:3.11-slim

WORKDIR /app

# Install system dependencies required for GeoPandas and NetworkX (if any)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
# Adding pytest and mlflow for the containerized tests
RUN pip install --no-cache-dir -r requirements.txt pytest httpx mlflow-skinny

# Download spaCy model explicitly
# (Fails gracefully if spacy isn't in requirements, but required for NLP module)
RUN pip install spacy==3.7.4 && python -m spacy download en_core_web_sm

# Copy the rest of the application
COPY . .

# Expose API and UI ports
EXPOSE 8000
EXPOSE 8501
