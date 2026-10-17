import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open("report.html", "r", encoding="utf-8") as f:
    html = f.read()

cards = re.findall(r'<div class="host-card">.*?<span class="host-card-name">(.*?)</span>.*?<span class="host-card-date">📅 (.*?)</span>.*?<div class="host-card-quote">"(.*?)"</div>.*?⏱️ (.*?) Watch', html, re.DOTALL)

print(f"Total Host Showcase Cards: {len(cards)}")
for idx, c in enumerate(cards, 1):
    print(f"{idx:2d}. {c[0]} | {c[1]} | {c[3]} | \"{c[2][:55]}...\"")
