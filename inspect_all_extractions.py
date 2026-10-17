import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("all_extracted_stocks.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print(f"Total videos in dataset: {len(data)}")

total_mentions = 0
all_comps = set()
disclosures = []

for vid, vdata in data.items():
    date = vdata.get('date')
    title = vdata.get('title')
    stocks = vdata.get('stocks', [])
    for s in stocks:
        comp = s.get('company')
        if comp and comp != 'N/A':
            total_mentions += 1
            all_comps.add(comp)
            if s.get('host_disclosed_holding'):
                disclosures.append((date, comp, s.get('disclosure_quote'), vid))

print(f"Total stock recommendations/analyses extracted: {total_mentions}")
print(f"Unique companies analyzed: {len(all_comps)}")
print("\nUnique Companies List:")
for c in sorted(all_comps):
    print(f"- {c}")

print(f"\nHost Disclosed Holdings ({len(disclosures)}):")
for d in disclosures:
    print(f"- [{d[0]}] {d[1]} (Video {d[3]}): \"{d[2]}\"")
