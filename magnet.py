#!/usr/bin/env python3
"""
Generator Script - Generate M3U playlist
"""

import json
import requests

def generate_m3u():
    url = "https://sayan-json-2.pages.dev/data/channels.json"
    print(f"[*] Fetching channels from API: {url}...")
    
    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        data = response.json()
        
        # The API returns a dictionary with 'channels' and 'cookies'
        channels = data.get("channels", [])
        cookies_data = data.get("cookies", {})
        # Cookie 'c' usually has acl=/* which works for all streams
        global_cookie = cookies_data.get("c", "")
        
        print(f"[+] Successfully fetched {len(channels)} channels.")
        
        m3u_file = "magnet.m3u"
        with open(m3u_file, "w", encoding="utf-8") as f:
            # EPG Source - Using sayanapp to better match these custom channel IDs
            f.write('#EXTM3U x-tvg-url="https://sayanapp.pages.dev/epg.xml.gz"\n\n')
            
            for ch in channels:
                channel_id = ch.get("id", "")
                name = ch.get("name", "Unknown Channel")
                logo = ch.get("logo", "")
                category = ch.get("category", "Sports")
                mpd = ch.get("url", "")
                
                # DRM Keys (Clearkey)
                drm1 = ch.get("drm1", "")
                drm2 = ch.get("drm2", "")
                
                # Skip invalid or empty URLs
                if not mpd or mpd.strip() == "":
                    continue
                    
                # Write EXTINF
                f.write(f'#EXTINF:-1 tvg-id="{channel_id}" tvg-logo="{logo}" group-title="{category}",{name}\n')
                
                # Add Clearkey DRM properties if keys are present
                if drm1 and drm2:
                    f.write('#KODIPROP:inputstream.adaptive.license_type=clearkey\n')
                    f.write(f'#KODIPROP:inputstream.adaptive.license_key={drm1}:{drm2}\n')
                
                # Construct stream URL with Cookies header for Kodi/OTT Navigator
                stream_url = mpd
                if global_cookie:
                    stream_url += f"|Cookie={global_cookie}"
                    
                f.write(f"{stream_url}\n\n")
                
        print(f"[*] Playlist generated successfully and saved to {m3u_file}")
        
    except Exception as e:
        print(f"[-] Error: {e}")
        # Optionally exit with 1 to fail the workflow if the fetch fails
        # exit(1) 

if __name__ == "__main__":
    generate_m3u()
