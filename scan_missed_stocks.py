import json
import os
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

with open("video_manifest.json", "r", encoding="utf-8") as f:
    manifest = json.load(f)

with open("all_extracted_stocks.json", "r", encoding="utf-8") as f:
    extractions = json.load(f)

# List of common stock names to scan in the transcripts of 0-stock videos
KNOWN_STOCKS = [
    'tata motors', 'reliance', 'tcs', 'infosys', 'hdfc', 'icici', 'sbi', 'itc', 'hul',
    'hindustan unilever', 'maruti', 'hyundai', 'paytm', 'zomato', 'swiggy', 'lic', 'nykaa',
    'policybazaar', 'cdsl', 'bse', 'mcx', 'cams', 'kfintech', 'angel one', 'irctc',
    'rvnl', 'irfc', 'pnb', 'bank of baroda', 'vodafone idea', 'idea', 'airtel', 'bharti airtel',
    'asian paints', 'pidilite', 'berger paints', 'titan', 'dmart', 'avenue supermarts',
    'wonderla', 'dreamfolks', 'relaxo', 'bata', 'sreeleathers', 'campus', 'indigo', 'spicejet',
    'yes bank', 'idfc first', 'kotak', 'axis bank', 'coal india', 'ongc', 'ntpc', 'power grid',
    'tata power', 'adani', 'adani enterprises', 'adani green', 'adani ports', 'mrf', 'apollo tyres',
    'voltas', 'blue star', 'havells', 'polycab', 'l&t', 'larsen'
]

zero_vids = [vid for vid, data in extractions.items() if not data.get("stocks")]
print(f"Checking transcripts of {len(zero_vids)} zero-stock videos for specific company names...")

missed_evaluations = []

for vid in zero_vids:
    tpath = f"transcripts_cache/{vid}.txt"
    if not os.path.exists(tpath):
        continue
    with open(tpath, "r", encoding="utf-8") as f:
        text = f.read().lower()
        
    found_stocks = []
    for s in KNOWN_STOCKS:
        # Search whole word
        pattern = r'\b' + re.escape(s) + r'\b'
        if re.search(pattern, text):
            found_stocks.append(s)
            
    if found_stocks:
        missed_evaluations.append({
            "video_id": vid,
            "date": manifest.get(vid, {}).get("date"),
            "title": manifest.get(vid, {}).get("title"),
            "found_stocks": found_stocks
        })

print(f"\nFound {len(missed_evaluations)} videos with 0 extracted stocks that actually mention specific companies!")
for m in missed_evaluations:
    print(f"{m['date']} | {m['video_id']} | {m['title'][:45]:45} | Stocks: {', '.join(m['found_stocks'])}")

