import json
import sys
import io
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

with open("potential_disclosures_audit.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# High-conviction filters: Look for phrases where speaker refers to himself owning/buying a specific stock
PRANJAL_FIRST_PERSON_PATTERNS = [
    r'मैंने\s+[^।\n]{0,35}(?:इन्वेस्ट किया|पैसा लगाया|खरीदा|लिया था|शेयर लिए|शेयर खरीदे)',
    r'मैं\s+[^।\n]{0,35}(?:इन्वेस्टेड हूँ|इन्वेस्टेड हूं|होल्ड करता|इन्वेस्ट हूँ|इन्वेस्ट हूं|बायस्ड हूँ|बायस्ड हूं)',
    r'(?:my|personally)\s+[^.\n]{0,35}(?:invested|bought|hold|portfolio|own|holding|bought shares)',
    r'मेरे\s+पोर्टफोलियो\s+में',
    r'मेरा\s+इन्वेस्टमेंट',
    r'पर्सनली\s+[^।\n]{0,25}(?:इन्वेस्ट|शेयर|खरीदा|होल्ड)',
]

results = []

for vid, triggers in data.items():
    for trig in triggers:
        txt = trig["full_context"]
        for pat in PRANJAL_FIRST_PERSON_PATTERNS:
            m = re.search(pat, txt, re.IGNORECASE)
            if m:
                # Exclude purely hypothetical phrases like "अगर मैंने", "मान लीजिए मैंने", "काश मैंने"
                if re.search(r'(?:अगर मैंने|मान लीजिए|सपोज मैंने|सोचिए मैंने|मान लो|इमेजिन)', txt):
                    continue
                results.append({
                    "video_id": vid,
                    "date": trig["date"],
                    "title": trig["title"],
                    "start": trig["start"],
                    "ts_str": trig["ts_str"],
                    "phrase": m.group(0),
                    "context": txt
                })
                break

print(f"High-conviction first-person ownership triggers: {len(results)}")

# Group by video
by_vid = {}
for r in results:
    vid = r["video_id"]
    if vid not in by_vid:
        by_vid[vid] = []
    by_vid[vid].append(r)

print(f"Unique videos: {len(by_vid)}")

# Check against existing 13 disclosures
with open("host_invested_disclosures.json", "r", encoding="utf-8") as f:
    existing = json.load(f)

existing_vids = set(existing.keys())

print(f"\n--- NEW VIDEOS NOT IN EXISTING 13 DISCLOSURES ---")
for vid, trigs in by_vid.items():
    if vid not in existing_vids:
        print(f"\nVideo: {vid} | Date: {trigs[0]['date']} | Title: {trigs[0]['title']}")
        for t in trigs[:3]:
            print(f"  [{t['ts_str']}] Phrase: '{t['phrase']}'")
            print(f"       Context: {t['context'][:140]}...")

