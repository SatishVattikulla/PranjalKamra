import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

with open("all_extracted_stocks.json", "r", encoding="utf-8") as f:
    extractions = json.load(f)

with open("video_manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Find all videos with stocks: []
empty_vids = [vid for vid, data in extractions.items() if not data.get("stocks")]
print(f"Total videos with empty stocks: {len(empty_vids)}")

# Let's inspect their titles
print("\n=== ALL VIDEOS WITH EMPTY STOCKS ===")
for idx, vid in enumerate(empty_vids, 1):
    meta = manifest.get(vid, {})
    title = meta.get("title", "")
    date = meta.get("date", "")
    print(f"{idx:3d}. [{date}] {vid}: {title}")

