import json

try:
    with open('playlists.json', 'r', encoding='utf-16') as f:
        data = json.load(f)
except Exception:
    with open('playlists.json', 'r', encoding='utf-8', errors='ignore') as f:
        data = json.load(f)

entries = data.get('entries', [])
print(f"Total playlists found: {len(entries)}")
for idx, p in enumerate(entries):
    title = p.get('title')
    pid = p.get('id')
    count = p.get('video_count')
    print(f"{idx+1}. {title} | ID: {pid} | Count: {count}")
