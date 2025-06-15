#!/bin/bash

# Create Python virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install required packages
pip install -r requirements.txt

# Create necessary directories
mkdir -p chroma_db

echo "Setup complete! To activate the environment, run: source venv/bin/activate" 