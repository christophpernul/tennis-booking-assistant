# Use Python 3.12 slim image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv package manager
RUN pip install uv

# Copy project files
COPY pyproject.toml .

# Install Python dependencies
RUN uv sync

# Copy application code
COPY . .

# Set environment variables
ENV PORT=8000
ENV SERVER_NAME="0.0.0.0"
ENV SERVER_PORT=8000

# Expose port
EXPOSE 8000

# Run the application
CMD ["uv", "run", "chainlit", "run", "run.py", "--host", "0.0.0.0", "--port", "8000"]
