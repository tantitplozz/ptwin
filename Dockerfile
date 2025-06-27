FROM python:3.12-slim

# Install system dependencies for Playwright and browser automation
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libdrm2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libxss1 \
    libnss3 \
    libgtk-3-0 \
    libgdk-pixbuf2.0-0 \
    libxinerama1 \
    libxcursor1 \
    libxi6 \
    libxext6 \
    libxfixes3 \
    libxrender1 \
    libcairo2 \
    libpango-1.0-0 \
    libatk1.0-0 \
    libcairo-gobject2 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium && \
    playwright install-deps chromium

# Copy application code
COPY . .

# Create directories for data persistence
RUN mkdir -p screenshots logs profiles

# Create non-root user for security
RUN useradd -m -u 1000 phantom && \
    chown -R phantom:phantom /app

# Switch to non-root user
USER phantom

# Expose WebSocket monitor port
EXPOSE 8686

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8686', timeout=5)" || exit 1

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Default command
CMD ["python", "phantom_autobuy/main.py"]