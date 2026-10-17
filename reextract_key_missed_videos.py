import io
import sys
import os
import re
import json
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

load_dotenv()

TARGET_VIDEOS = [
    "vZ4GmabcqEQ", # Hyundai IPO
    "4jZTIeLpK44", # Stocks that I Avoid
    "4X0Jy4_HaOs", # Do you own these stocks ? Here is why you should Exit !
    "fx2GUJVxv6A", # Truth about BIG Upcoming IPOs of 2021
    "-IK0YuOKiTA", # Why Airlines Go Bankrupt ?
    "3eAO7o2J1wM", # What is Coffee Can Investing ?
    "YzXEFrEaq34", # Why I Reject Some Good Stocks ?
    "BXPPUsXUl7A"  # My Complete Stock Selection Process Explained
]

MANIFEST_FILE = "video_manifest.json"
CACHE_DIR = "transcripts_cache"
OUTPUT_FILE = "all_extracted_stocks.json"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    manifest = json.load(f)

with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
    all_extractions = json.load(f)

SYSTEM_PROMPT = """You are an expert equity research analyst.
Analyze the provided transcript of an Indian stock market video by Pranjal Kamra.
Extract every listed stock, company, or upcoming IPO that is specifically evaluated, analyzed, cited as a cautionary/exit example, or recommended.

For each stock/company, return a JSON object with:
1. "company": Standard commercial English company name (e.g., "Hyundai Motor India", "Vodafone Idea", "State Bank of India", "Bank of Baroda", "Zee Entertainment", "InterGlobe Aviation", "Asian Paints", "Pidilite Industries", "Titan Company", "Zomato", "Life Insurance Corporation of India").
2. "view": "Positive", "Negative", or "Neutral".
3. "growth_reasons": Why Pranjal has this view (thesis, valuation concerns, debt, liquidity shock, monopsony buyer risk, governance, moat, etc.).
4. "promoter_details": Promoter or governance notes mentioned. If none, write "Not explicitly discussed in video".
5. "host_disclosed_holding": true ONLY if Pranjal explicitly says he personally owns/bought shares. Otherwise false.
6. "disclosure_quote": Verbatim quote if host_disclosed_holding is true, else "".

Output MUST be a JSON array: [ { ... }, { ... } ]
Return raw JSON only, no markdown formatting.
"""

MODELS = [
    'gemini-3.5-flash-lite',
    'gemini-3.6-flash',
    'gemini-3.7-flash',
    'gemini-3.1-flash-lite',
    'gemini-2.5-flash-lite'
]

def extract_for_video(vid):
    tpath = f"{CACHE_DIR}/{vid}.txt"
    if not os.path.exists(tpath):
        print(f"Missing transcript for {vid}")
        return []
    with open(tpath, "r", encoding="utf-8") as f:
        text = f.read()
    
    meta = manifest.get(vid, {})
    title = meta.get("title", "")
    date = meta.get("date", "")
    print(f"\nProcessing {vid} ({date}): '{title}' ({len(text)} chars)...")
    
    prompt = f"Video Title: {title}\nPublish Date: {date}\nTranscript:\n{text[:28000]}"
    
    for model_name in MODELS:
        try:
            print(f"  Trying model: {model_name}...")
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    temperature=0.1,
                    response_mime_type="application/json"
                )
            )
            raw = response.text.strip()
            # Clean possible markdown fences
            if raw.startswith("```"):
                raw = re.sub(r"^```(?:json)?", "", raw)
                raw = re.sub(r"```$", "", raw).strip()
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                print(f"  Successfully extracted {len(parsed)} stocks!")
                return parsed
            elif isinstance(parsed, dict) and "stocks" in parsed:
                return parsed["stocks"]
            else:
                print(f"  Unexpected JSON shape: {type(parsed)}")
                return []
        except Exception as e:
            print(f"  Failed with {model_name}: {e}")
            time.sleep(2)
            continue
    return []

new_additions_count = 0
for vid in TARGET_VIDEOS:
    stocks = extract_for_video(vid)
    if stocks:
        all_extractions[vid] = {
            "video_id": vid,
            "title": manifest.get(vid, {}).get("title"),
            "date": manifest.get(vid, {}).get("date"),
            "stocks": stocks
        }
        new_additions_count += len(stocks)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
            json.dump(all_extractions, out, indent=2, ensure_ascii=False)
        print(f"Updated {OUTPUT_FILE} for {vid}")
    time.sleep(3)

print(f"\nFinished! Added {new_additions_count} new stock evaluations.")
