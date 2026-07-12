#!/bin/bash
echo "Installing Playwright browsers..."
python -m playwright install --with-deps chromium
echo "Starting main.py..."
python main.py
