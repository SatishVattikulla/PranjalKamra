import json
from youtube_transcript_api import YouTubeTranscriptApi

test_vids = [
    ("X_WrSKHYVfg", "Sreeleathers"),
    ("sMFP8VaqrBY", "10 Types of Stocks that I Like"),
    ("yqXNlYiEzYQ", "2 Reasons I Never buy Reliance Shares"),
    ("45KFq23IGcY", "How I lost Money in YES Bank 5 Years Ago"),
    ("62G_uwiMGiI", "D-mart business Plan")
]

api = YouTubeTranscriptApi()

for vid, title in test_vids:
    print(f"\nTesting Video: {title} ({vid})")
    try:
        transcript_list = api.list_transcripts(vid)
        available = []
        for t in transcript_list:
            available.append(f"{t.language_code} ({'manual' if not t.is_generated else 'auto'})")
        print(f"  Available transcripts: {', '.join(available)}")
        
        # Try fetching Hindi or English
        t = transcript_list.find_transcript(['hi', 'en', 'hi-Latn'])
        data = t.fetch()
        print(f"  Successfully fetched transcript! Segments: {len(data)}")
        first_few = " ".join([d['text'] for d in data[:5]])
        print(f"  Sample snippet: {first_few[:120]}...")
    except Exception as e:
        print(f"  Failed: {e}")
