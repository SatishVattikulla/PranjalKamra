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

inspect_video("Y2OfXN4jvn0", 430, 450)
inspect_video("45KFq23IGcY", 130, 155)
inspect_video("aQQ1JthC0f8", 1000, 1025)
inspect_video("T-nmNeW8AM4", 925, 955)
inspect_video("d5PNNxsPwX4", 35, 60)
inspect_video("c7g74-hekAE", 1140, 1165)
inspect_video("E7Aexkdko8A", 85, 110)
