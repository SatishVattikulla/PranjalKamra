import json

with open("channel_videos_v2.json", "r", encoding="utf-16") as f:
    data = json.load(f)

entries = data.get("entries", [])
print(f"Total videos: {len(entries)}")

durations = [e.get('duration') for e in entries if e.get('duration') is not None]
avg_duration_sec = sum(durations) / len(durations) if durations else 0
avg_duration_min = avg_duration_sec / 60
total_duration_hours = sum(durations) / 3600 if durations else 0

print(f"Average duration: {avg_duration_min:.1f} minutes ({avg_duration_sec:.0f} seconds)")
print(f"Total video duration across all 229 videos: {total_duration_hours:.1f} hours")
