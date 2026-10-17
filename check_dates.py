import subprocess
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Total entries: {len(entries)}")

# Test checking upload dates for the first 10 videos
for i in range(10):
    vid = entries[i]['id']
    title = entries[i]['title']
    cmd = ["yt-dlp", "--dump-json", "--no-download", f"https://www.youtube.com/watch?v={vid}"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if res.returncode == 0:
        info = json.loads(res.stdout)
        print(f"[{i+1}] {info.get('upload_date')} | {vid} | {title}")
    else:
        print(f"[{i+1}] Failed for {vid}: {res.stderr}")
