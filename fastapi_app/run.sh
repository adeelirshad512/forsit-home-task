#!/bin/bash
set -e

PROJECT_DIR="$(dirname "$(realpath "$0")")"

if [ ! -d "$PROJECT_DIR" ]; then
    echo "Error: Project directory not found"
    exit 1
fi

cd "$PROJECT_DIR" || { echo "Error: Cannot cd to project directory"; exit 1; }

if ! command -v python3 &> /dev/null || ! python3 --version | grep -q "3.10"; then
    echo "Error: Python 3.10+ required"
    exit 1
fi

if ! python3 -m venv --help > /dev/null 2>&1; then
    echo "python3.10-venv not installed, installing..."
    sudo apt update
    sudo apt install -y python3.10-venv || { echo "Error: Failed to install python3.10-venv"; exit 1; }
fi

echo "Checking virtual environment..."
FORCE_RECREATE=$1

if [ "$FORCE_RECREATE" = "--force" ] || [ ! -f "venv/bin/activate" ]; then
    echo "Creating fresh virtual environment..."
    rm -rf venv
    python3 -m venv venv || { echo "Error: Failed to create virtual environment"; exit 1; }
else
    echo "Virtual environment exists and looks valid, skipping creation"
fi

source venv/bin/activate || { echo "Error: Failed to activate virtual environment"; exit 1; }

echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install --upgrade pip || { echo "Error: Failed to upgrade pip"; exit 1; }
    pip install -r requirements.txt || { echo "Error: Failed to install requirements"; exit 1; }
else
    echo "Error: requirements.txt not found"
    exit 1
fi

echo "Configuring environment..."
if [ ! -f ".env" ]; then
    echo "Error: .env file not found. Please create .env with DATABASE_URL and API_KEY"
    exit 1
else
    echo "Using existing .env file"
fi

PORT=8000
MAX_PORT=8010

function port_in_use() {
    lsof -iTCP:"$1" -sTCP:LISTEN -t >/dev/null
}

while port_in_use $PORT; do
    echo "Port $PORT is busy, trying next port..."
    PORT=$((PORT + 1))
    if [ $PORT -gt $MAX_PORT ]; then
        echo "Error: No free port found between 8000 and $MAX_PORT"
        exit 1
    fi
done

echo "Starting FastAPI server on port $PORT..."
echo "Press Ctrl+C to stop the server"
uvicorn app.main:app --host 0.0.0.0 --port $PORT || { echo "Error: Failed to start FastAPI server. Check app/logs/app.log"; exit 1; }
