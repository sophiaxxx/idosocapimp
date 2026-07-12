#!/bin/bash
echo "Installing dependencies..."
apt-get update -qq && apt-get install -y -qq xvfb > /dev/null 2>&1
echo "Installing Playwright browsers..."
python -m playwright install --with-deps chromium
echo "Starting main.py with xvfb-run..."
export DISPLAY=:99
xvfb-run --auto-servernum --server-args="-screen 0 1280x720x24 -nolisten tcp -ac" python main.py
