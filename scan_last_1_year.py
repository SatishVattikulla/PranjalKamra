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

# The target cutoff date is 1 year ago from Oct 17, 2026: i.e., Oct 1, 2025 or Oct 17, 2025 (e.g. 20251001)
CUTOFF_DATE = "20251001"
print(f"Scanning videos from latest down to cutoff: {CUTOFF_DATE}...")

last_year_videos = []

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    for idx, e in enumerate(entries):
        vid = e.get('id')
        if not vid:
            continue
        
        # Check manifest cache
        if vid in manifest and manifest[vid].get('upload_date'):
            ud = manifest[vid]['upload_date'].replace("-", "")
            title = manifest[vid].get('title')
        else:
            time.sleep(0.5)
            try:
                info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)
                ud = info.get('upload_date')
                title = info.get('title')
                formatted_date = f"{ud[:4]}-{ud[4:6]}-{ud[6:]}" if ud else "2026-01-01"
                manifest[vid] = {
                    "video_id": vid,
                    "title": title,
                    "date": formatted_date,
                    "upload_date": formatted_date,
                    "duration": info.get('duration')
                }
                # Save incremental
                with open(MANIFEST_FILE, "w", encoding="utf-8") as f:
                    json.dump(manifest, f, indent=2, ensure_ascii=False)
            except Exception as ex:
                print(f"[{idx+1}] Error for {vid}: {ex}")
                continue

        print(f"[{idx+1}] {ud} | {vid} | {title[:55]}")
        
        if ud and ud < CUTOFF_DATE:
            print(f"\nReached video earlier than {CUTOFF_DATE} ({ud}). Stopping scan.")
            break
            
        last_year_videos.append(manifest[vid])

print(f"\nTotal videos in the last 1 year (since Oct 2025): {len(last_year_videos)}")
