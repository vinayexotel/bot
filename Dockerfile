# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (optional: pandas & openpyxl might need these)
RUN apt-get update && apt-get install -y build-essential gcc && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of your app
COPY . .

# Expose the port
ENV PORT=8080
EXPOSE $PORT

# Use a simpler startup command for better reliability
CMD gunicorn --bind :$PORT --workers 1 --threads 4 --timeout 120 app:app

