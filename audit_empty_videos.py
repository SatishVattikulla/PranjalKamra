import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("video_manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

with open("all_extracted_stocks.json", "r", encoding="utf-8") as f:
    extractions = json.load(f)

stock_vids = set()
for vid, data in extractions.items():
    if data.get("stocks") and len(data["stocks"]) > 0:
        stock_vids.add(vid)

print(f"Total videos in manifest: {len(manifest)}")
print(f"Videos with extracted stocks: {len(stock_vids)}")
print(f"Videos with 0 stocks: {len(manifest) - len(stock_vids)}")

# Inspect titles of 0-stock videos that might have had stocks
potential_missed_vids = []
for vid, meta in manifest.items():
    if vid not in stock_vids:
        title = meta.get("title", "")
        # Check if title mentions stock, share, IPO, or company names
        keywords = ['stock', 'share', 'ipo', 'company', 'shares', 'stocks', 'invest', 'portfolio', 'multibagger', 'dividend']
        matched = [k for k in keywords if k in title.lower()]
        if matched:
            potential_missed_vids.append((vid, meta.get("date"), title, matched))

print(f"\n0-stock videos whose titles contain stock-related keywords: {len(potential_missed_vids)}")
for v in potential_missed_vids[:35]:
    print(f"  {v[1]} | {v[0]} | {v[2]} (matched: {v[3]})")

