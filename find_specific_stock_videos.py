import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])

specific_keywords = [
    'portfolio', 'bought', 'buying', 'i buy', 'i bought', 'my stock',
    'holding', 'disclose', 'shares i', 'multibagger', 'stocks for',
    'top stock', 'best stock', 'stocks to buy', 'hidden gem', 'monopoly'
]

print("=== Targeted Stock / Portfolio / Buying Videos ===")
count = 0
for idx, entry in enumerate(entries):
    t = entry.get('title', '')
    tl = t.lower()
    if any(k in tl for k in specific_keywords):
        count += 1
        print(f"{count}. {t} (ID: {entry.get('id')})")
