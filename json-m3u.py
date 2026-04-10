#!/usr/bin/env python3
"""
Quick JSON to M3U Converter - Simple Version
Just download and convert - no frills!
"""

import json
import requests

# Fetch JSON
print("Fetching channels...")
url = "https://raw.githubusercontent.com/dilzyking/Allrounder/refs/heads/main/api/jiotv2.json"
response = requests.get(url)
channels = response.json()

# Create M3U
m3u = "#EXTM3U\n"
for ch in channels:
    m3u += f'#EXTINF:-1 tvg-id="{ch['channel_id']}" tvg-name="{ch['channel_name']}" tvg-logo="{ch['channel_logo']}" group-title="{ch['channel_genre']}",{ch['channel_name']}\n'
    m3u += ch['channel_url'] + "\n"

# Save
with open('Sportlink.m3u', 'w', encoding='utf-8') as f:
    f.write(m3u)

print(f"✅ Created Sportlink.m3u with {len(channels)} channels!")