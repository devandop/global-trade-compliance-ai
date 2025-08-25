#!/bin/bash

# Define the path to the virtual environment's python executable
VENV_PYTHON="venv/bin/python"

# --- Check if the venv python executable exists ---
if [ ! -f "$VENV_PYTHON" ]; then
    echo "ERROR: The Python executable in the virtual environment was not found."
    echo "Please run './setup.sh' first to create the environment."
    exit 1
fi

echo "Using Python from: $VENV_PYTHON"
echo "Starting development servers..."

# Start the FastAPI backend server in the background
echo "Starting FastAPI backend on http://localhost:8000"
"$VENV_PYTHON" -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload &
FASTAPI_PID=$!
sleep 5

# Start the Streamlit frontend server in the foreground
echo "Starting Streamlit frontend on http://localhost:8501"
# --- THIS LINE IS THE FIX ---
"$VENV_PYTHON" -m streamlit run frontend/app.py --server.port 8501 --server.enableCORS true

# This part runs after you stop Streamlit (Ctrl+C)
echo "Streamlit frontend stopped. Shutting down FastAPI backend..."
kill $FASTAPI_PID
echo "Servers stopped."
