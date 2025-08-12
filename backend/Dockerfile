# backend/Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Copy requirements first
COPY requirements.txt .

# Install system dependencies before Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Now install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all source files
COPY . .

# Start backend server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
