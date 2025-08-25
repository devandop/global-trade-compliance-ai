FROM python:3.9-slim-buster

# --- ROBUST NODE.JS & NPM INSTALLATION ---
# 1. Install necessary dependencies for adding new repositories (like curl)
RUN apt-get update && apt-get install -y --no-install-recommends curl gnupg && rm -rf /var/lib/apt/lists/*

# 2. Add the official NodeSource repository for Node.js v18 (LTS)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash -

# 3. Install Node.js and npm from the newly added repository
RUN apt-get install -y nodejs
# --- END NODE.JS INSTALLATION ---

# Set the working directory inside the container
WORKDIR /app

# Copy requirements files first to leverage Docker's build cache
COPY backend/requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY backend/ ./backend/
COPY portia-agent/ ./portia-agent/

# Expose the port the app will run on
EXPOSE 8000

# The command to run the application in production
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
