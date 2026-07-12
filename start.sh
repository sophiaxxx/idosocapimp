#!/bin/bash
echo "Installing dependencies..."
apt-get update -qq && apt-get install -y -qq xvfb > /dev/null 2>&1
echo "Installing Playwright browsers..."
python -m playwright install --with-deps chromium
echo "Starting main.py..."
python main.py
