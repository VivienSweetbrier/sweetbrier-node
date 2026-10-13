import requests
import sys

clip_id = "1UxKB1ow8KTyCcp2"
api_url = f"https://studio-api.suno.ai/api/external/clips/?ids={clip_id}"

try:
    print("Bypassing yt-dlp liability blocklist...")
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if data and len(data) > 0:
            audio_url = data[0].get('audio_url')
            if audio_url:
                print(f"Found CDN Link: {audio_url}")
                print("Downloading audio payload...")
                audio_data = requests.get(audio_url).content
                with open("civic_defense.mp3", "wb") as f:
                    f.write(audio_data)
                print("Download complete: civic_defense.mp3")
            else:
                print("Audio URL not found in the payload. The track may not be public.")
        else:
            print("No data returned for that ID. Is the link correct?")
    else:
        print(f"API rejected request: {response.status_code}")
except Exception as e:
    print(f"Sweetbrier Override Failed: {e}")
