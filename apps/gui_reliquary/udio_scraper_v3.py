import requests
import re
import json

url = "https://www.udio.com/songs/1UKQpMJrtLU4jGny4LnC3Y"
headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get(url, headers=headers)
audio_url = None

match = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', resp.text, re.DOTALL)
if match:
    try:
        data = json.loads(match.group(1))
        audio_url = data.get('props', {}).get('pageProps', {}).get('song', {}).get('song_path')
    except: pass

if not audio_url:
    urls = re.findall(r'https://[^"\']*?\.mp3', resp.text)
    if urls: audio_url = urls[0]

if audio_url:
    print(f"Found audio URL: {audio_url}")
    with open("clankina_theme.mp3", "wb") as f:
        f.write(requests.get(audio_url).content)
    print("Download complete: clankina_theme.mp3")
