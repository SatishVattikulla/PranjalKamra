import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('host_invested_disclosures.json', 'r', encoding='utf-8') as f:
    disclosures = json.load(f)

print("=== VERIFIED HOST PERSONAL DISCLOSURES (PAST 1 YEAR) ===")
for vid, items in disclosures.items():
    for item in items:
        print(f"Company: {item['company']}")
        print(f"Date:    {item['date']}")
        print(f"Time:    {item['timestamp_str']} ({item['timestamp_sec']}s)")
        print(f"Quote:   \"{item['disclosure_quote']}\"")
        print(f"Link:    {item['youtube_link']}")
        print("-" * 60)
