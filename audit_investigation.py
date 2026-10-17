import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

with open('host_invested_disclosures.json', 'r', encoding='utf-8') as f:
    disclosures = json.load(f)

print("=== CHECKING TIMESTAMPS PRECISION ===")
for vid, items in disclosures.items():
    seg_file = f'transcripts_cache/{vid}_segments.json'
    if not os.path.exists(seg_file):
        print(f"Missing segment file: {seg_file}")
        continue
    with open(seg_file, 'r', encoding='utf-8') as sf:
        segments = json.load(sf)
    for it in items:
        q = it.get('disclosure_quote', '')
        words = [w for w in q.replace('।', ' ').replace('?', ' ').replace(',', ' ').split() if len(w) >= 3]
        best_match = None
        best_score = 0
        best_idx = -1
        for i in range(len(segments)):
            window_text = ' '.join(s.get('text', '') for s in segments[i:i+5])
            score = sum(1 for w in words if w in window_text)
            if score > best_score:
                best_score = score
                best_match = segments[i]
                best_idx = i
        
        assigned_ts = it.get('timestamp_sec')
        found_ts = int(best_match['start']) if best_match else -1
        diff = abs(assigned_ts - found_ts)
        comp_name = it.get('company', '')
        ts_str = it.get('timestamp_str', '')
        found_str = f"{found_ts//60:02d}:{found_ts%60:02d}" if found_ts >= 0 else "N/A"
        print(f"{vid} | {comp_name[:30]:30} | Assigned: {assigned_ts:4d}s ({ts_str}) | Found: {found_ts:4d}s ({found_str}) | Diff: {diff:3d}s | Score: {best_score}/{len(words)}")
        if best_match:
            print(f"   Spoken snippet: {' '.join(s.get('text', '') for s in segments[best_idx:best_idx+3])[:120]}")

