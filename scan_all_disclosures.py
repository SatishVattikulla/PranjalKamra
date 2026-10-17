import glob
import json
import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

manifest = {}
if os.path.exists("video_manifest.json"):
    with open("video_manifest.json", "r", encoding="utf-8") as f:
        manifest = json.load(f)

# Patterns that indicate personal investment / holding
DISCLOSURE_PATTERNS = [
    r'(?:मैं|मैंने|पर्सनली|खुद)\s*[^।\n]{0,50}(?:इन्वेस्ट|इन्वेस्टेड|खरीदा|लिया था|होल्ड|लगाया था|पैसा लगाया|पोर्टफोलियो)',
    r'(?:my|personally)\s*[^.\n]{0,50}(?:invested|bought|hold|portfolio|own|holding)',
    r'(?:डिस्क्लेमर|डिस्क्लोज़र|disclaimer|disclosure)[^।\n]{0,60}(?:invested|holding|shares|buy|bought|इन्वेस्ट|होल्ड|शेयर)',
    r'(?:biased|बायस्ड)[^।\n]{0,40}(?:invested|इन्वेस्ट|शेयर|holding)'
]

files = glob.glob("transcripts_cache/*_segments.json")
print(f"Scanning {len(files)} transcript segment files for potential personal disclosures...")

candidates = []

for fpath in files:
    vid = os.path.basename(fpath).replace("_segments.json", "")
    with open(fpath, "r", encoding="utf-8") as sf:
        segments = json.load(sf)
        
    for i in range(len(segments)):
        # Check window of 3 segments
        window_text = " ".join(s.get("text", "") for s in segments[i:i+3])
        st = segments[i].get("start", 0)
        
        for pat in DISCLOSURE_PATTERNS:
            m = re.search(pat, window_text, re.IGNORECASE)
            if m:
                matched_phrase = m.group(0)
                # Filter out generic educational disclaimers like "यह कोई बाय सेल रिकमेंडेशन नहीं है" without personal ownership
                candidates.append({
                    "video_id": vid,
                    "date": manifest.get(vid, {}).get("date", "Unknown"),
                    "title": manifest.get(vid, {}).get("title", "Unknown"),
                    "start": st,
                    "ts_str": f"{int(st//60):02d}:{int(st%60):02d}",
                    "match": matched_phrase,
                    "full_context": window_text
                })
                break

print(f"Total potential raw disclosure triggers found: {len(candidates)}")

# Group by video
by_vid = {}
for c in candidates:
    vid = c["video_id"]
    if vid not in by_vid:
        by_vid[vid] = []
    by_vid[vid].append(c)

print(f"Videos with potential triggers: {len(by_vid)}")

# Output sample triggers
with open("potential_disclosures_audit.json", "w", encoding="utf-8") as out:
    json.dump(by_vid, out, indent=2, ensure_ascii=False)

print("Saved detailed trigger log to potential_disclosures_audit.json")
