import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('transcripts_cache/M_npo4c9DEA_segments.json', 'r', encoding='utf-8') as f:
    segs = json.load(f)

for s in segs:
    txt = s['text'].lower()
    if 'बायस्ड' in txt or 'इन्वेस्टेड' in txt or 'biased' in txt or 'बीएसई' in txt:
        sec = int(s['start'])
        m = sec // 60
        sec_rem = sec % 60
        print(f"{m:02d}:{sec_rem:02d} ({sec}s): {s['text']}")
