import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

for m in ["gemini-3.8-flash", "gemini-2.5-flash-lite", "gemini-3.5-flash-lite", "gemini-2.5-pro"]:
    try:
        res = client.models.generate_content(
            model=m,
            contents="Hello! Confirm status ok in JSON: {\"status\": \"ok\"}"
        )
        print(f"Model {m}: SUCCESS -> {res.text.strip()}")
    except Exception as e:
        print(f"Model {m}: FAILED -> {e}")
