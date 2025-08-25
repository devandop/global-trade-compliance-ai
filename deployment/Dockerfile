# --- Stage 1: Build Stage ---
# CORRECTED: Use Python 3.12 as the base image to meet Portia SDK requirements.
FROM python:3.12-bullseye AS builder

# Set environment variables for non-interactive installs and Python best practices.
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# The canonical, robust way to install system packages in a single layer.
# This updates, installs, and cleans up in one atomic operation.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Verify Node.js installation as a sanity check.
RUN node -v && npm -v

# Create a virtual environment for Python packages.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory.
WORKDIR /app

# Install Python dependencies into the virtual environment.
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Production Image ---
# CORRECTED: Use the corresponding slim version of Python 3.12 for the final image.
FROM python:3.12-slim-bullseye AS final

# Set the same non-interactive env var.
ENV DEBIAN_FRONTEND=noninteractive

# Install only the necessary RUNTIME system dependencies (nodejs).
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create a dedicated, non-root user for security.
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# Copy the pre-built virtual environment from the builder stage.
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code.
COPY --chown=appuser:appuser backend/ ./backend/
COPY --chown=appuser:appuser portia_agent/ ./portia_agent/

# Set the PATH to include the virtual environment's binaries.
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the application will listen on.
EXPOSE 8000

# The command to run the application in production.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
