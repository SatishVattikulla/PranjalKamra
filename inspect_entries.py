import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Total videos in playlist: {len(entries)}")

print("\n--- 10 Oldest Videos in this list ---")
for i, v in enumerate(entries[-10:][::-1]):
    print(f"{i+1}. Title: {v.get('title')} | ID: {v.get('id')} | URL: https://youtu.be/{v.get('id')}")
