import io
import sys
import os
import json
import http.cookiejar
import requests
from youtube_transcript_api import YouTubeTranscriptApi

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

jar = http.cookiejar.MozillaCookieJar("cookies.txt")
jar.load(ignore_discard=True, ignore_expires=True)
session = requests.Session()
session.cookies = jar
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36'
})
api = YouTubeTranscriptApi(http_client=session)

test_vids = [
    ("sMFP8VaqrBY", "10 Types of Stocks that I Like"),
    ("yqXNlYiEzYQ", "2 Reasons I Never buy Reliance Shares"),
    ("45KFq23IGcY", "How I lost Money in YES Bank 5 Years Ago"),
    ("62G_uwiMGiI", "D-mart business Plan")
]

for vid, title in test_vids:
    print(f"\nVideo: {title} ({vid})")
    try:
        tlist = api.list(vid)
        tracks = [f"{t.language_code} ({'manual' if not t.is_generated else 'auto'})" for t in tlist]
        print(f"  Tracks: {', '.join(tracks)}")
        
        # Prefer Hindi or English
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
                available = list(tlist)
                if available:
                    transcript = available[0]
        
        if transcript:
            data = transcript.fetch()
            # check type of items
            first_item = data[0]
            if hasattr(first_item, 'text'):
                text = " ".join([x.text for x in data])
            else:
                text = " ".join([x.get('text', '') for x in data])
            print(f"  Fetched {len(data)} segments, {len(text)} chars!")
            print(f"  Snippet: {text[:150]}...")
    except Exception as e:
        print(f"  Failed: {e}")
