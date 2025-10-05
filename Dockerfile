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
COPY uv.lock* .

# Install Python dependencies
RUN uv sync --frozen

# Copy application code
COPY src/ ./src/
COPY run.py .

# Set environment variables
ENV PORT=8080
ENV GRADIO_SERVER_NAME="0.0.0.0"
ENV GRADIO_SERVER_PORT=8080

# Expose port
EXPOSE 8080

# Run the application
CMD ["uv", "run", "python", "run.py"]