import yt_dlp
import json

ydl_opts = {
    'quiet': True,
    'extract_flat': False,
    'skip_download': True,
    'cookiefile': 'cookies.txt',
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
    }
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info("https://www.youtube.com/watch?v=X_WrSKHYVfg", download=False)
        print("Success! Upload date:", info.get('upload_date'))
        print("Title:", info.get('title'))
except Exception as e:
    print("Error:", e)
