import subprocess
import json

cmd = [
    "yt-dlp",
    "--flat-playlist",
    "--dump-single-json",
    "https://www.youtube.com/@pranjalkamra/videos"
]

print("Fetching videos list from @pranjalkamra...")
res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
if res.returncode != 0:
    print("Error:", res.stderr)
else:
    with open("channel_videos.json", "w", encoding="utf-8") as f:
        f.write(res.stdout)
    print("Saved channel_videos.json successfully.")
