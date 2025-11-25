#!/bin/bash

# Quick start script for AI Project Generator on macOS/Linux

echo ""
echo "===================================================="
echo "   AI Project Generator - Quick Start"
echo "===================================================="
echo ""

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Install Python 3.11+ first."
    exit 1
fi

python3 --version

echo "[OK] Python found"
echo ""

# Check if venv exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv
source venv/bin/activate

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1

if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies"
    exit 1
fi

echo "[OK] Dependencies installed"
echo ""

# Check .env file
if [ ! -f ".env" ]; then
    echo "WARNING: .env file not found"
    echo "Creating .env from template..."
    cp .env.example .env
    echo "IMPORTANT: Edit .env and add your GitHub token for full functionality"
fi

echo ""
echo "===================================================="
echo "Starting AI Project Generator..."
echo "===================================================="
echo ""

# Terminal 1: Backend
echo "Starting Backend on http://localhost:8000"
echo "To start Frontend in another terminal:"
echo "  source venv/bin/activate"
echo "  streamlit run frontend/app.py"
echo ""

python backend/main.py

# Deactivate venv on exit
deactivate
