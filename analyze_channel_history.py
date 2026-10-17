import json

with open("channel_videos.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Total videos uploaded: {len(entries)}")

# Sort by upload date or index
# Note: flat-playlist usually returns latest first
if entries:
    print(f"Latest video: {entries[0].get('title')} (ID: {entries[0].get('id')})")
    print(f"Earliest video: {entries[-1].get('title')} (ID: {entries[-1].get('id')})")

print("\n--- Earliest 10 Videos ---")
for i, v in enumerate(entries[-10:][::-1]):
    print(f"{i+1}. Title: {v.get('title')} | ID: {v.get('id')} | URL: https://youtu.be/{v.get('id')}")

print("\n--- Search for keywords in titles: 'portfolio', 'stock', 'buying', 'bought', 'disclose', 'invest', 'shares' ---")
keywords = ['portfolio', 'bought', 'buying', 'my stock', 'holding', 'share', 'invest']
matching = []
for v in entries:
    t = v.get('title', '').lower()
    if any(k in t for k in keywords):
        matching.append(v)

print(f"Found {len(matching)} videos with investment/portfolio keywords out of {len(entries)} total.")
print("Sample 15 title matches:")
for v in matching[:15]:
    print(f"- {v.get('title')} ({v.get('id')})")
