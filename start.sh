#!/bin/bash
echo "Installing Playwright Chromium..."
python -m playwright install chromium --with-deps
echo "Starting main.py..."
python main.py
