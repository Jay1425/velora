#!/bin/bash
# Render Build Script
# This script runs during deployment to set up the application

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Build complete!"
