# --- Stage 1: Build Stage ---
# Use a modern, stable Debian base image ("Bullseye") for better package repository reliability.
FROM python:3.9-bullseye AS builder

# Set environment variables to ensure apt-get runs non-interactively and for Python best practices.
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# The canonical, robust way to install system packages in a single layer.
# This updates, installs, and cleans up in one atomic operation.
# We install 'build-essential' here in the builder stage in case any Python
# packages need to compile C extensions.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Verify Node.js installation as a sanity check
RUN node -v && npm -v

# Create a virtual environment for Python packages for proper isolation.
# /opt/ is a standard location for optional software.
RUN python -m venv /opt/venv
# Activate the virtual environment for subsequent RUN commands
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

# Install Python dependencies
# Copy only the requirements file first to leverage Docker's build cache.
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Production Image ---
# Start the final stage from a fresh, clean SLIM base image for a smaller size.
FROM python:3.9-slim-bullseye AS final

# Set the same non-interactive env var
ENV DEBIAN_FRONTEND=noninteractive

# Install only the necessary RUNTIME system dependencies.
# We need nodejs for the Portia SDK to run the Xero MCP server.
# We do NOT need build-essential, curl, etc., keeping the image slim and secure.
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    nodejs \
    && rm -rf /var/lib/apt/lists/*

# Create a dedicated, non-root user for running the application for security.
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# Copy the pre-built virtual environment from the builder stage.
COPY --from=builder /opt/venv /opt/venv

# Copy the application source code, setting ownership to the non-root user.
COPY --chown=appuser:appuser backend/ ./backend/
COPY --chown=appuser:appuser portia-agent/ ./portia-agent/

# Set the PATH to include the virtual environment's binaries for the final image.
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the application will listen on.
EXPOSE 8000

# The command to run the application in production.
# The --reload flag is NOT used in production.
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
