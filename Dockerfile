# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies including Node.js
RUN apt-get update && apt-get install -y \
    curl \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && node --version && npm --version \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
COPY pyproject.toml .
COPY uv.lock .

# Copy requirements and install Python dependencies
RUN pip install uv
RUN uv pip install --no-cache-dir --system -r requirements.txt

# Copy source code and configuration
COPY src/ ./src/
COPY .env* ./
# COPY .env .env

# Set environment variables for Streamlit
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Expose the port Streamlit runs on
EXPOSE 8501

# Set the working directory to src where main.py is located
WORKDIR /app/src

# Health check for the Streamlit app
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Run the Streamlit application
CMD ["streamlit", "run", "main.py"]