#!/bin/bash
# Daily GitHub Trending Digest Runner
# Run this script daily to fetch and send the digest

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

# Load environment variables from .env file if exists
if [ -f "$SKILL_DIR/.env" ]; then
    export $(cat "$SKILL_DIR/.env" | grep -v '^#' | xargs)
fi

# Debug: show channel
echo "NOTIFY_CHANNEL=$NOTIFY_CHANNEL"

# Run the fetch script
python3 "$SCRIPT_DIR/fetch_trending.py" --notify
