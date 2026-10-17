with open('transcripts_cache/737SS12ZvYo.txt', 'r', encoding='utf-8') as f:
    text = f.read()

import re
keywords = ['tata', 'reliance', 'infosys', 'hdfc', 'icici', 'itc', 'hul', 'maruti', 'dmart', 'pidilite', 'asian paints', 'bata', 'relaxo', 'sreeleathers', 'colgate', 'nestle', 'britannia', 'wipro', 'tcs', 'brain', 'focus']

for kw in keywords:
    m = re.findall(rf'\b{kw}\b', text, re.IGNORECASE)
    if m:
        print(f'Found {kw}: {len(m)} times')
