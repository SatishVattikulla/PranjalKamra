import json
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def inspect_video(vid, min_s, max_s):
    with open(f"transcripts_cache/{vid}_segments.json", "r", encoding="utf-8") as f:
        segs = json.load(f)
    print(f"\n=== Video {vid} ({min_s}s - {max_s}s) ===")
    for s in segs:
        st = s.get("start", 0)
        if min_s <= st <= max_s:
            print(f"  {int(st//60):02d}:{int(st%60):02d} ({int(st)}s): {s.get('text')}")

# Check BSE in M_npo4c9DEA
inspect_video("M_npo4c9DEA", 975, 1010)

# Check NSE in M_npo4c9DEA
inspect_video("M_npo4c9DEA", 1025, 1050)

# Check Parag Parikh in abcih589JUg
inspect_video("abcih589JUg", 760, 795)

# Check CDSL / BSE in vu0bSw_z63U
inspect_video("vu0bSw_z63U", 240, 275)

# Check Wonderla in Y2OfXN4jvn0
inspect_video("Y2OfXN4jvn0", 2170, 2195)
