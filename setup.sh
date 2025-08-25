#!/bin/bash
echo "Creating Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt
echo "Installing frontend dependencies..."
pip install -r frontend/requirements.txt
echo "Setup complete. Activate with 'source venv/bin/activate'."
