# Use Python 3.10 as base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install wait-for-it script
RUN wget -O /usr/local/bin/wait-for-it https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh \
    && chmod +x /usr/local/bin/wait-for-it

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Check if .env file exists
RUN if [ ! -f ".env" ]; then \
        echo "⚠️  .env file not found, creating from .env.example..."; \
        if [ -f ".env.example" ]; then \
            cp .env.example .env; \
            echo "✅ Created .env from .env.example"; \
        else \
            echo "❌ No .env or .env.example file found!"; \
            exit 1; \
        fi; \
    else \
        echo "✅ .env file found"; \
    fi

# Validate required environment variables
RUN if ! grep -q "OPENAI_API_KEY=" .env; then \
        echo "⚠️  OPENAI_API_KEY not found in .env"; \
    else \
        echo "✅ Environment variables look good"; \
    fi

# Expose port
EXPOSE 8000

# Start command - no longer need to wait for Qdrant since we're using Qdrant Cloud
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 