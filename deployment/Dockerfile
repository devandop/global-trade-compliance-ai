# --- Stage 1: Build Stage ---
# Use a specific, stable Python version as the base
FROM python:3.9-slim-buster AS builder

# Set environment variables for non-interactive installs
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set an environment variable for the Node.js version for easy updates
ENV NODE_VERSION 18.17.1

# This is the official SHA256 checksum for node-v18.17.1-linux-x64.tar.xz
# Source: https://nodejs.org/dist/v18.17.1/SHASUMS256.txt
ENV NODE_SHA256 59413a6c93223f5397063625405459f0f62b8001d8b746d5c560f772b38c20c1

# Install necessary dependencies for building and downloading
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl tar xz-utils && \
    rm -rf /var/lib/apt/lists/*

# Download the official Node.js binary, verify its checksum, and install it
RUN curl -fsSL "https://nodejs.org/dist/v${NODE_VERSION}/node-v${NODE_VERSION}-linux-x64.tar.xz" -o nodejs.tar.xz && \
    # --- Checksum Verification Step ---
    echo "${NODE_SHA256}  nodejs.tar.xz" | sha256sum -c - && \
    # --- End Verification ---
    tar -xJf nodejs.tar.xz -C /usr/local --strip-components=1 && \
    rm nodejs.tar.xz && \
    ln -s /usr/local/bin/node /usr/local/bin/nodejs

# Verify the installation
RUN node -v && npm -v

# Set the working directory
WORKDIR /app

# Install Python dependencies into a virtual environment for isolation
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements file and install dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt


# --- Stage 2: Final Production Stage ---
# Use a fresh, clean base image for the final product
FROM python:3.9-slim-buster AS final

# Create a non-root user for better security
RUN useradd --create-home appuser
WORKDIR /home/appuser/app
USER appuser

# Copy the virtual environment from the build stage
COPY --from=builder /opt/venv /opt/venv

# Copy the application code from the current build context
COPY --chown=appuser:appuser backend/ ./backend/
COPY --chown=appuser:appuser portia-agent/ ./portia-agent/

# Set the PATH to include the virtual environment's binaries
ENV PATH="/opt/venv/bin:$PATH"

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application in production
# We do not use --reload in production
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
