# ==============================================================================
# Aesthetic Physique Builder - Production Container Image
# Multi-platform Web Portals (Athlete Companion & Operations Console)
# ==============================================================================

FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8550

# Install required system libraries for Flet web runtime
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    libgl1 \
    libglib2.0-0 \
    libasound2 \
    && rm -rf /var/lib/apt/lists/*

# Set up non-root application user
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app -s /sbin/nologin appuser

WORKDIR /app

# Cache dependency installation layer
COPY frontend_app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy complete application codebase
COPY . /app/

# Ensure appropriate permissions for application user
RUN chown -R appuser:appgroup /app

USER appuser

# Expose web portal port
EXPOSE 8550

# Health check to ensure web server is responding
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8550/ || exit 1

# Launch the Web Portals in production server mode
CMD ["python", "run_ecosystem.py", "--web", "--port", "8550"]
