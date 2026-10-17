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

MANIFEST_FILE = "video_manifest.json"
CACHE_DIR = "transcripts_cache"
OUTPUT_FILE = "all_extracted_stocks.json"

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
    manifest = json.load(f)

# Target videos from last 1 year (2025-10-01 to today)
target_videos = [v for v in manifest.values() if v.get('date', '') >= "2025-10-01"]
target_videos.sort(key=lambda x: x['date'], reverse=True)

# Load existing extractions if resuming
extractions = {}
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            extractions = json.load(f)
    except Exception:
        extractions = {}

SYSTEM_INSTRUCTION = """You are an institutional financial analyst and bilingual NLP extraction engine.
Analyze the provided YouTube video transcript from Indian finance educator Pranjal Kamra (in Hindi, Hinglish, and English).

Your task is to identify and extract EVERY specific Indian listed stock/company analyzed, recommended, evaluated, or discussed in this episode.

For each stock, extract:
1. "company": The official commercial English name of the company (e.g. "Avenue Supermarts", "Sreeleathers", "Reliance Industries", "Tata Motors", "ITC", "Infosys", "CDSL", "HDFC Bank"). Normalize spoken Hindi/Devanagari names to English.
2. "view": The speaker's overall stance - MUST be strictly one of: "Positive", "Negative", or "Neutral".
3. "growth_reasons": Detailed thesis, business model moat, valuation rationale, ROE/ROCE metrics, margin trends, revenue targets, or specific catalysts/risks discussed by Pranjal.
4. "promoter_details": Details mentioned regarding promoters, management credibility, insider actions, promoter holding %, or corporate governance. If not explicitly discussed, write "Not explicitly discussed in video".
5. "host_disclosed_holding": Boolean true or false. True ONLY if Pranjal explicitly discloses on camera that HE HIMSELF personally bought, holds, invested in, or sold shares of this company for his personal portfolio or family account (e.g., "मैंने खुद खरीदा", "मेरे पास ये शेयर है", "I picked this stock", "In my portfolio").
6. "disclosure_quote": If host_disclosed_holding is true, provide the exact verbatim spoken sentence/quote (in Hindi/English) where he states his personal ownership. If false, leave as empty string "".

RULES:
- Do NOT extract general macroeconomic indices (Nifty, Sensex, Bank Nifty, S&P 500).
- Do NOT extract mutual fund names (e.g. "Parag Parikh Flexi Cap Fund") as individual stocks, unless an underlying equity company is being analyzed.
- If the video is purely about insurance, real estate, government schemes, or general personal budgeting without analyzing any individual listed stock, return an empty list: []
- Output MUST be valid, parseable JSON only. No markdown fences.
"""

def clean_json_response(text: str) -> list:
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        return json.loads(text)
    except Exception as e:
        cleaned = re.sub(r',\s*([\]}])', r'\1', text)
        return json.loads(cleaned)

MODELS = ["gemini-3.8-flash", "gemini-2.5-flash-lite", "gemini-3.5-flash-lite"]

print(f"Total videos to extract: {len(target_videos)}")
print(f"Already extracted: {len(extractions)} videos")

for idx, v in enumerate(target_videos, 1):
    vid = v['video_id']
    date = v['date']
    title = v['title']
    
    if vid in extractions:
        print(f"[{idx}/{len(target_videos)}] Already extracted: {vid} ({date})")
        continue
        
    txt_path = os.path.join(CACHE_DIR, f"{vid}.txt")
    if not os.path.exists(txt_path) or os.path.getsize(txt_path) < 50:
        print(f"[{idx}/{len(target_videos)}] No transcript yet for {vid}. Skipping.")
        continue
        
    with open(txt_path, "r", encoding="utf-8") as tf:
        transcript_text = tf.read()
        
    print(f"[{idx}/{len(target_videos)}] Extracting {vid} ({date}) | '{title[:40]}...' ({len(transcript_text)} chars)...", end=" ", flush=True)
    
    prompt = f"Video Title: {title}\nVideo Upload Date: {date}\n\nTranscript:\n{transcript_text[:35000]}"
    
    success = False
    
    for model_name in MODELS:
        try:
            time.sleep(4.0)
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION,
                    response_mime_type="application/json"
                )
            )
            
            parsed = clean_json_response(response.text)
            extractions[vid] = {
                "video_id": vid,
                "title": title,
                "date": date,
                "stocks": parsed
            }
            
            # Save incrementally
            with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
                json.dump(extractions, out_f, indent=2, ensure_ascii=False)
                
            stocks_found = [s.get('company') for s in parsed]
            disclosed = [s.get('company') for s in parsed if s.get('host_disclosed_holding')]
            print(f"-> SUCCESS via {model_name} ({len(parsed)} stocks: {stocks_found[:3]}) [Disclosed: {disclosed}]")
            success = True
            break
        except Exception as e:
            print(f"[{model_name} err: {e}]", end=" ", flush=True)
            time.sleep(3)
            
    if not success:
        print(f"\nFailed to extract {vid} across all available models.")

print(f"\nAll extractions complete! Saved to {OUTPUT_FILE}")
