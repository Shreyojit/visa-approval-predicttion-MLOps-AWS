# Stage 1: Builder for compiling dependencies
FROM python:3.10-slim-buster as builder

WORKDIR /app
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential libpq-dev && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Runtime environment
FROM python:3.10-slim-buster

# Create non-root user
RUN addgroup --system app && adduser --system --ingroup app appuser
USER appuser

WORKDIR /app
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Copy only necessary files from builder
COPY --from=builder --chown=appuser:app /home/appuser/.local /home/appuser/.local
COPY --chown=appuser:app . .

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

EXPOSE 8080

# Use Gunicorn as production server
CMD ["gunicorn", "app:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]