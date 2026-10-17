import json
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])

stock_keywords = [
    r'portfolio', r'stock', r'share', r'invest', r'buying', r'bought', 
    r'multibagger', r'dividend', r'nifty', r'sensex', r'sector', r'ipo',
    r'd-mart', r'tata', r'reliance', r'itc', r'hdfc', r'infy', r'icici',
    r'monopoly', r'small cap', r'mid cap', r'large cap', r'penny',
    r'crore', r'wealth', r'fund', r'hidden'
]

pattern = re.compile('|'.join(stock_keywords), re.IGNORECASE)

stock_videos = []
for idx, entry in enumerate(entries):
    title = entry.get('title', '')
    if pattern.search(title):
        stock_videos.append(entry)

print(f"Total videos: {len(entries)}")
print(f"Videos with stock/investing keywords in title: {len(stock_videos)}")

print("\n--- Sample Titles of Stock/Investing Videos (First 30) ---")
for i, v in enumerate(stock_videos[:30]):
    print(f"{i+1}. {v.get('title')} | ID: {v.get('id')}")
