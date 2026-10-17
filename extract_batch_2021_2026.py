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

# Target videos from 2021-01-01 to 2026-10-31
target_videos = [v for v in manifest.values() if v.get('date', '') >= "2021-01-01"]
target_videos.sort(key=lambda x: x['date'], reverse=True)

# Load existing extractions
extractions = {}
if os.path.exists(OUTPUT_FILE):
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            extractions = json.load(f)
    except Exception:
        extractions = {}

SYSTEM_INSTRUCTION = """You are an institutional financial analyst and bilingual NLP extraction engine.
Analyze the provided YouTube video transcripts from Indian finance educator Pranjal Kamra (in Hindi, Hinglish, and English).

You will be given up to 3 videos. For each video, identify and extract EVERY specific Indian listed stock/company analyzed, recommended, evaluated, or discussed in that video.

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
- If a video is purely about insurance, real estate, government schemes, or general personal budgeting without analyzing any individual listed stock, return an empty list: [] for that video.
- Output MUST be valid, parseable JSON dictionary where keys are the respective video IDs:
{
  "VIDEO_ID_1": [ { ... } ],
  "VIDEO_ID_2": [ { ... } ]
}
No markdown fences. Raw JSON only.
"""

def clean_json_response(text: str) -> dict:
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

MODELS = [
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.7-flash",
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-2.5-flash-lite",
    "gemini-3.8-flash"
]

def main():
    pending_videos = []
    for v in target_videos:
        vid = v['video_id']
        if vid not in extractions:
            txt_path = os.path.join(CACHE_DIR, f"{vid}.txt")
            if os.path.exists(txt_path) and os.path.getsize(txt_path) > 50:
                pending_videos.append(v)

    print(f"Total target videos (2021-2026): {len(target_videos)}")
    print(f"Already extracted: {len(extractions)}")
    print(f"Pending to extract with transcripts: {len(pending_videos)}")

    BATCH_SIZE = 3
    for b_idx in range(0, len(pending_videos), BATCH_SIZE):
        batch = pending_videos[b_idx:b_idx+BATCH_SIZE]
        vids_in_batch = [b['video_id'] for b in batch]
        
        prompt_parts = ["Analyze the following videos and extract stock mentions according to the instructions:\n"]
        for b in batch:
            vid = b['video_id']
            date = b['date']
            title = b['title']
            txt_path = os.path.join(CACHE_DIR, f"{vid}.txt")
            with open(txt_path, "r", encoding="utf-8") as tf:
                t_text = tf.read()
            prompt_parts.append(f"--- VIDEO ID: {vid} ---\nTitle: {title}\nDate: {date}\nTranscript:\n{t_text[:20000]}\n--- END VIDEO {vid} ---\n")
            
        full_prompt = "\n".join(prompt_parts)
        print(f"[{b_idx+1}/{len(pending_videos)}] Processing Batch: {vids_in_batch}...", end=" ", flush=True)
        
        success = False
        for model_name in MODELS:
            try:
                time.sleep(4.0)
                response = client.models.generate_content(
                    model=model_name,
                    contents=full_prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        response_mime_type="application/json"
                    )
                )
                
                parsed_dict = clean_json_response(response.text)
                
                # Assign to each video in batch
                for b in batch:
                    vid = b['video_id']
                    stocks_for_vid = parsed_dict.get(vid, [])
                    if isinstance(stocks_for_vid, dict):
                        stocks_for_vid = [stocks_for_vid]
                    extractions[vid] = {
                        "video_id": vid,
                        "title": b['title'],
                        "date": b['date'],
                        "stocks": stocks_for_vid
                    }
                    
                # Save incremental
                with open(OUTPUT_FILE, "w", encoding="utf-8") as out_f:
                    json.dump(extractions, out_f, indent=2, ensure_ascii=False)
                    
                total_batch_stocks = sum(len(extractions[v]['stocks']) for v in vids_in_batch)
                print(f"-> SUCCESS via {model_name} ({total_batch_stocks} total stocks across batch)")
                success = True
                break
            except Exception as e:
                print(f"[{model_name} err: {e}]", end=" ", flush=True)
                time.sleep(4)
                
        if not success:
            print(f"\nFailed batch {vids_in_batch}")

    print(f"\nAll batches processed! Saved {len(extractions)} total extractions to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
