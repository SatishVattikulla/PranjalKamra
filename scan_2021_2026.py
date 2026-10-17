import io
import sys
import os
import json
import time
import yt_dlp

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Total entries in channel list: {len(entries)}")

MANIFEST_FILE = "video_manifest.json"
manifest = {}
if os.path.exists(MANIFEST_FILE):
    try:
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception:
        manifest = {}

ydl_opts = {
    'quiet': True,
    'extract_flat': False,
    'skip_download': True,
    'cookiefile': 'cookies.txt',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
}

CUTOFF_DATE = "20210101"
print(f"Scanning videos from latest down to cutoff: {CUTOFF_DATE}...")

vids_2021_2026 = []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for idx, e in enumerate(entries):
        vid = e.get('id')
        if not vid:
            continue
        
        # Check manifest cache
        if vid in manifest and manifest[vid].get('date'):
            ud = manifest[vid]['date'].replace("-", "")
            title = manifest[vid].get('title')
        else:
            time.sleep(0.4)
            try:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
                ud = info.get('upload_date')
                title = info.get('title')
                formatted_date = f"{ud[:4]}-{ud[4:6]}-{ud[6:]}" if ud else "2021-01-01"
                manifest[vid] = {
                    "video_id": vid,
                    "title": title,
                    "date": formatted_date,
                    "upload_date": formatted_date,
                    "duration": info.get('duration')
                }
                # Save incremental every 5 entries
                if idx % 5 == 0:
                    with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
                        json.dump(manifest, f, indent=2, ensure_ascii=False)
            except Exception as ex:
                print(f"[{idx+1}] Error for {vid}: {ex}")
                continue

        if idx % 10 == 0 or (ud and ud < CUTOFF_DATE):
            print(f"[{idx+1}/{len(entries)}] {ud} | {vid} | {title[:45]}")
        
        if ud and ud < CUTOFF_DATE:
            print(f"\nReached video earlier than {CUTOFF_DATE} ({ud}). Stopping scan.")
            break
            
        vids_2021_2026.append(manifest[vid])

# Final save
with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)

print(f"\nTotal videos between 2021 and 2026: {len(vids_2021_2026)}")
