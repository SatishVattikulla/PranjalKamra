import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

with open(r"C:\Users\vatti\.gemini\antigravity\brain\9af766bd-dc14-4fa9-a4fb-ed01da0f8e58\.system_generated\steps\871\content.md", "r", encoding="utf-8") as f:
    text = f.read()

for key in ['dateText', 'publishDate', 'uploadDate', 'datePublished', 'published']:
    matches = re.findall(rf'"{key}":\s*"([^"]+)"', text)
    print(key, matches[:5])

# Also check dateText simpleText
m_simple = re.findall(r'"dateText":\{"simpleText":"([^"]+)"\}', text)
print("dateText simpleText:", m_simple)

# Check itemProp datePublished
m_prop = re.findall(r'itemprop="datePublished" content="([^"]+)"', text)
print("itemprop datePublished:", m_prop)

# Check uploadDate itemprop
m_up = re.findall(r'itemprop="uploadDate" content="([^"]+)"', text)
print("itemprop uploadDate:", m_up)
