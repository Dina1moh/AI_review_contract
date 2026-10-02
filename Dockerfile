# Use an official, stable Python runtime based on Debian for maximum compatibility
FROM python:3.11-slim

# Set system environment variables to optimize Python inside Docker
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_LINK_MODE=copy

# Install essential system dependencies required for compiling heavy legal/AI packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv installer directly inside the global container space for ultra-fast performance
RUN pip install --no-cache-dir uv

# Set the working directory inside the container
WORKDIR /app

# Copy only the requirements file first to utilize Docker caching mechanisms
COPY requirements.txt .

# Install dependencies globally inside the container environment using uv syntax
RUN uv pip install --system -r requirements.txt

# Copy the entire project code into the container app directory
COPY . .

# Expose port 8000 for the FastAPI live application server
EXPOSE 8000

# Default command to run the backend application (can be overridden during execution)
CMD ["python", "src/application_contract_review/api.py"]
