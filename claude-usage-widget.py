#!/usr/bin/env python3
"""
Claude Code Usage Widget
Fetches usage data from Anthropic API and displays 5H%, WK%, and reset time
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from urllib.request import Request, urlopen
from urllib.error import URLError

# Cache file and duration
CACHE_FILE = Path.home() / ".claude" / ".usage-cache.json"
CACHE_DURATION = 300  # 5 minutes

def get_cached_data():
    """Get cached usage data if still valid."""
    if not CACHE_FILE.exists():
        return None

    try:
        with open(CACHE_FILE, 'r') as f:
            cache = json.load(f)

        # Check if cache is still valid
        if time.time() - cache.get('timestamp', 0) < CACHE_DURATION:
            return cache.get('data')
    except:
        pass

    return None

def save_cache(data):
    """Save usage data to cache."""
    try:
        cache = {
            'timestamp': time.time(),
            'data': data
        }
        CACHE_FILE.parent.mkdir(exist_ok=True)
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache, f)
    except:
        pass

def get_access_token():
    """Read access token from Claude credentials."""
    creds_file = Path.home() / ".claude" / ".credentials.json"

    try:
        with open(creds_file, 'r') as f:
            creds = json.load(f)

        # Try different possible locations for the token
        token = (creds.get('claudeAiOauth', {}).get('accessToken') or
                creds.get('access_token') or
                creds.get('token'))

        return token
    except:
        return None

def fetch_usage_data(token):
    """Fetch usage data from Anthropic API."""
    url = "https://api.anthropic.com/api/oauth/usage"

    headers = {
        'Authorization': f'Bearer {token}',
        'anthropic-beta': 'oauth-2025-04-20',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'User-Agent': 'claude-code/2.0'
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=5) as response:
            data = json.load(response)
            return data
    except URLError:
        return None

def format_time_until_reset(reset_time_str):
    """Calculate and format time until reset."""
    try:
        reset_time = datetime.fromisoformat(reset_time_str.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        delta = reset_time - now

        total_seconds = int(delta.total_seconds())
        if total_seconds < 0:
            return "0m"

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60

        if hours > 0:
            return f"{hours}h{minutes}m"
        else:
            return f"{minutes}m"
    except:
        return "?"

def main():
    """Main function to generate usage widget output."""

    # Try cache first
    cached = get_cached_data()
    if cached:
        usage_data = cached
    else:
        # Fetch from API
        token = get_access_token()
        if not token:
            print("ERR:NO_TOKEN", end='')
            return

        usage_data = fetch_usage_data(token)
        if not usage_data:
            print("ERR:API", end='')
            return

        # Save to cache
        save_cache(usage_data)

    # Extract data
    five_hour = usage_data.get('five_hour', {})
    seven_day = usage_data.get('seven_day', {})

    five_hour_pct = int(five_hour.get('utilization', 0))
    seven_day_pct = int(seven_day.get('utilization', 0))
    reset_time = five_hour.get('resets_at', '')

    time_until_reset = format_time_until_reset(reset_time)

    # Format output
    output = f"5H:{five_hour_pct}% WK:{seven_day_pct}% RST:{time_until_reset}"
    print(output, end='')

if __name__ == "__main__":
    main()
