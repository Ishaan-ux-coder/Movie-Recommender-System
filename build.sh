#!/bin/bash
# Exit on error
set -o errexit

# Install Frontend dependencies (lightweight)
pip install -r requirements.txt

# Install Backend dependencies (Heavy ML libs) - ONLY for Render
echo "Installing Backend ML dependencies..."
pip install fastapi==0.111.0 uvicorn==0.30.1 httpx==0.27.0 pandas==2.2.2 numpy==2.0.1 scipy==1.13.1 scikit-learn==1.5.1 nltk==3.8.1 gunicorn

# Rebuild Data
echo "Rebuilding Pickles..."
python rebuild_pickles.py
