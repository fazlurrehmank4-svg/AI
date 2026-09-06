#!/usr/bin/env bash
# CropGuard AI 1-Click Startup Script for Linux / macOS / Cloud
set -e

echo "🌱 Starting CropGuard AI Production Engine..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate || source venv/Scripts/activate

echo "Installing / verifying dependencies..."
pip install -r requirements.txt

echo "Launching FastAPI AI Backend on http://0.0.0.0:8000..."
uvicorn Backend.app:app --host 0.0.0.0 --port 8000 --reload
