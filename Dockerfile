# Dockerfile - robust install Dockerfile for rubixe (updated)
FROM python:3.11-slim

LABEL maintainer="you@example.com"

ENV DEBIAN_FRONTEND=noninteractive
ENV PIP_DEFAULT_TIMEOUT=120
ENV PIP_NO_CACHE_DIR=1
ENV PYTHONUNBUFFERED=1

# 1) Install system packages useful for builds & healthchecks
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
      build-essential \
      libopenblas-dev \
      liblapack-dev \
      libomp-dev \
      curl \
      wget \
      ca-certificates \
      git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements files (if present)
COPY requirements.txt /app/requirements.txt
COPY requirements_heavy.txt /app/requirements_heavy.txt

# Upgrade pip / setuptools / wheel
RUN python -m pip install --upgrade pip setuptools wheel

# Install light dependencies first (if present)
RUN if [ -f /app/requirements.txt ]; then \
      pip install --no-cache-dir -r /app/requirements.txt ; \
    else \
      echo "no requirements.txt found; skipping lighter dependencies"; \
    fi

# Install heavy dependencies with retries (if present)
RUN if [ -f /app/requirements_heavy.txt ]; then \
      set -ex; attempts=5; delay=10; \
      for i in $(seq 1 $attempts); do \
        echo "Attempt $i to install heavy packages"; \
        pip install --no-cache-dir --prefer-binary -r /app/requirements_heavy.txt && break || true; \
        echo "Install attempt $i failed — sleeping $delay seconds"; \
        sleep $delay; delay=$((delay*2)); \
      done; \
    else \
      echo "no requirements_heavy.txt found; skipping heavy deps"; \
    fi

# Copy application code
COPY . /app

# Ensure docs dir exists and writable
RUN mkdir -p /app/docs && chown -R root:root /app/docs

# default workdir already /app
# Keep a neutral default CMD; compose overrides this per-service
CMD ["bash", "-lc", "echo 'Default container: no command specified. Use docker-compose to run backend or frontend.' && tail -f /dev/null"]
