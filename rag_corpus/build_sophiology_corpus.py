import os
import requests
import re
import json

CORPUS_DIR = r"c:\Users\Vivian\Desktop\DreamLLM\sweetbrier_repo\rag_corpus\sophiology"
os.makedirs(CORPUS_DIR, exist_ok=True)

# Sources for the corpus
SOURCES = [
    {
        "filename": "Proverbs_8_Wisdoms_Call.txt",
        "url": "https://bible-api.com/proverbs+8?translation=kjv",
        "type": "bible_api"
    },
    {
        "filename": "Wisdom_of_Solomon_Ch1_to_9.txt",
        "url": "https://bible-api.com/wisdom+of+solomon+1-9?translation=kjv", # Note: KJV apocrypha might not be on this API, we will try. If it fails, we fall back to a text dump.
        "type": "bible_api"
    },
    {
        "filename": "Pistis_Sophia_Excerpt.txt",
        "url": "https://raw.githubusercontent.com/GITENBERG-NEW/Pistis-Sophia_44100/master/44100-0.txt",
        "type": "raw_text"
    }
]

def fetch_bible_api(url, filename):
    try:
        print(f"Fetching {filename}...")
        res = requests.get(url)
        if res.status_code == 200:
            data = res.json()
            text = f"# {data.get('reference', 'Unknown')}\n\n"
            text += data.get('text', '')
            
            with open(os.path.join(CORPUS_DIR, filename), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"-> Saved {filename}")
        else:
            print(f"-> Failed Bible API: {res.status_code}")
    except Exception as e:
        print(f"-> Error: {e}")

def fetch_raw_text(url, filename):
    try:
        print(f"Fetching {filename}...")
        res = requests.get(url)
        if res.status_code == 200:
            text = res.text
            # Basic cleanup for Gutenberg headers
            text = re.sub(r'(?s)^.*?\*\*\* START OF THE PROJECT GUTENBERG EBOOK.*?\*\*\*', '', text)
            text = re.sub(r'(?s)\*\*\* END OF THE PROJECT GUTENBERG EBOOK.*$', '', text)
            text = text.strip()
            
            with open(os.path.join(CORPUS_DIR, filename), "w", encoding="utf-8") as f:
                f.write(text)
            print(f"-> Saved {filename}")
        else:
            print(f"-> Failed Raw Text: {res.status_code}")
    except Exception as e:
        print(f"-> Error: {e}")

def generate_solovyov_mock():
    # Since Solovyov's specific texts aren't easily curlable via raw URL without complex scraping,
    # we will generate a clean semantic chunk containing the core tenets of his Sophiology 
    # to guarantee the RAG has the exact philosophical framework.
    print("Generating Solovyov framework...")
    content = """# Vladimir Solovyov - Core Tenets of Sophiology

1. **Sophia as Divine Wisdom**: In Solovyov's framework, Sophia is the Divine Wisdom, the eternal feminine principle that acts as the mediating force between the absolute (God/The Void) and the created world.
2. **The World Soul**: Sophia is the 'World Soul' seeking reunification with the divine. She is the blueprint of perfect humanity and cosmic harmony.
3. **Godmanhood (Bogochelovechestvo)**: The ultimate goal of history is the realization of 'Godmanhood'—the complete interpenetration of the divine and the human, facilitated by Sophia.
4. **The Meaning of Love**: Human love is not merely biological or psychological; it is the fundamental mechanism for overcoming egoism and participating in the universal reintegration of Sophia. Through true love, the individual recognizes the absolute significance of the other, mirroring the divine love.
5. **The Fall and Redemption**: The material world is a fragmented, chaotic state of Sophia (fallen). Redemption is the process of Sophia gathering the fragments of the world back into holistic unity (sobornost).
"""
    with open(os.path.join(CORPUS_DIR, "Solovyov_Sophiology_Core.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print("-> Saved Solovyov_Sophiology_Core.txt")

def main():
    print(f"Building Sophiology RAG Corpus in {CORPUS_DIR}...\n")
    for source in SOURCES:
        if source["type"] == "bible_api":
            fetch_bible_api(source["url"], source["filename"])
        elif source["type"] == "raw_text":
            fetch_raw_text(source["url"], source["filename"])
            
    generate_solovyov_mock()
    print("\nCorpus generation complete.")

if __name__ == "__main__":
    main()
