FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.11-slim

WORKDIR /code

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Make sure scripts in .local are usable
ENV PATH=/root/.local/bin:$PATH

# Copy application
COPY . .

# Create non-root user
RUN addgroup --system app && adduser --system --group app
RUN chown -R app:app /code
USER app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health/ || exit 1

EXPOSE 8000