import requests
import re
import json

url = "https://www.udio.com/songs/fbFgxXZbzcd4zdBNfohZDy"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
print("Fetching Udio page...")
try:
    resp = requests.get(url, headers=headers)
    
    # Try finding __NEXT_DATA__
    audio_url = None
    match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', resp.text, re.DOTALL)
    if match:
        try:
            data = json.loads(match.group(1))
            props = data.get('props', {}).get('pageProps', {})
            song = props.get('song', {})
            audio_url = song.get('song_path')
        except:
            pass
            
    if not audio_url:
        print("Fallback to regex scan...")
        # Fallback regex for cdn links
        urls = re.findall(r'https://[^"\']*?\.mp3', resp.text)
        if urls:
            audio_url = urls[0]
            
    if audio_url:
        print(f"Found audio URL: {audio_url}")
        audio_data = requests.get(audio_url).content
        with open("civic_defense.mp3", "wb") as f:
            f.write(audio_data)
        print("Download complete: civic_defense.mp3")
    else:
        print("Could not locate audio URL in page source.")
except Exception as e:
    print(f"Extraction failed: {e}")
