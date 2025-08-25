# Use a specific, stable Python version
FROM python:3.9-slim-buster

# Install Node.js and npm for the Xero MCP server
RUN apt-get update && \
    apt-get install -y --no-install-recommends nodejs npm && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements files first to leverage Docker's build cache
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY backend/ ./backend/
COPY portia-agent/ ./portia-agent/

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application in production
# We do not use --reload in production
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
