import yt_dlp
import json

ydl_opts = {
    'quiet': True,
    'extract_flat': False,
    'skip_download': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("https://www.youtube.com/watch?v=X_WrSKHYVfg", download=False)
    print("Upload date:", info.get('upload_date'))
    print("Title:", info.get('title'))
