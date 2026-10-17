import json
import sys

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])
with open("all_titles.txt", "w", encoding="utf-8") as out:
    for i, e in enumerate(entries):
        out.write(f"{i+1}. [{e.get('id')}] {e.get('title')}\n")

print(f"Dumped {len(entries)} titles into all_titles.txt")
