import json

with open("host_invested_disclosures.json", "r", encoding="utf-8") as f:
    disclosures = json.load(f)

for vid, items in disclosures.items():
    for item in items:
        if item.get("company") == "BSE Ltd.":
            item["timestamp_sec"] = 995
            item["timestamp_str"] = "16:35"
            item["youtube_link"] = f"https://youtu.be/{vid}?t=995s"

with open("host_invested_disclosures.json", "w", encoding="utf-8") as f:
    json.dump(disclosures, f, indent=2, ensure_ascii=False)

print("Updated BSE Ltd. timestamp to 16:35 (995s) successfully!")
