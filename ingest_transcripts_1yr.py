import io
import sys
import os
import json
import time
import http.cookiejar
import requests
from youtube_transcript_api import YouTubeTranscriptApi

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MANIFEST_FILE = "video_manifest.json"
CACHE_DIR = "transcripts_cache"
COOKIES_FILE = "cookies.txt"

os.makedirs(CACHE_DIR, exist_ok=True)

with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Filter for videos from last 1 year (date >= 2025-10-01)
target_videos = [v for v in manifest.values() if v.get('date', '') >= "2025-10-01"]
target_videos.sort(key=lambda x: x['date'], reverse=True)

print(f"Total targeted videos in last 1 year: {len(target_videos)}")

# Set up authenticated session
jar = http.cookiejar.MozillaCookieJar(COOKIES_FILE)
jar.load(ignore_discard=True, ignore_expires=True)
session = requests.Session()
session.cookies = jar
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
})

api = YouTubeTranscriptApi(http_client=session)

success_count = 0
fail_count = 0

for idx, v in enumerate(target_videos, 1):
    vid = v['video_id']
    title = v['title']
    date = v['date']
    txt_path = os.path.join(CACHE_DIR, f"{vid}.txt")
    seg_path = os.path.join(CACHE_DIR, f"{vid}_segments.json")
    
    # Check if already cached
    if os.path.exists(txt_path) and os.path.getsize(txt_path) > 100:
        print(f"[{idx}/{len(target_videos)}] Cached: {vid} ({date}) | {title[:40]}...")
        success_count += 1
        continue
        
    print(f"[{idx}/{len(target_videos)}] Fetching: {vid} ({date}) | {title[:40]}...", end=" ", flush=True)
    time.sleep(1.0) # polite rate limit
    
    try:
        tlist = api.list(vid)
        transcript = None
        for lang in ['hi', 'en']:
            try:
                transcript = tlist.find_transcript([lang])
                break
            except Exception:
                pass
        if not transcript:
            try:
                transcript = tlist.find_generated_transcript(['hi', 'en'])
            except Exception:
                avail = list(tlist)
                if avail:
                    transcript = avail[0]
                    
        if not transcript:
            print("-> No transcript available.")
            fail_count += 1
            continue
            
        data = transcript.fetch()
        
        # Save raw segments
        seg_data = []
        full_text_parts = []
        for item in data:
            if hasattr(item, 'text'):
                t_str = item.text
                start = getattr(item, 'start', 0)
                duration = getattr(item, 'duration', 0)
            else:
                t_str = item.get('text', '')
                start = item.get('start', 0)
                duration = item.get('duration', 0)
            seg_data.append({"start": start, "duration": duration, "text": t_str})
            full_text_parts.append(t_str)
            
        full_text = " ".join(full_text_parts)
        
        with open(txt_path, "w", encoding="utf-8") as tf:
            tf.write(full_text)
            
        with open(seg_path, "w", encoding="utf-8") as sf:
            json.dump(seg_data, sf, ensure_ascii=False)
            
        print(f"-> SUCCESS ({len(seg_data)} segments, {len(full_text)} chars)")
        success_count += 1
    except Exception as e:
        print(f"-> FAILED: {e}")
        fail_count += 1

print(f"\nFinished transcript ingestion! Success: {success_count}, Failed: {fail_count}")
