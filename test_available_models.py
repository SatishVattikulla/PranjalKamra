import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

candidate_models = [
    "gemini-2.0-flash",
    "gemini-2.0-flash-lite",
    "gemini-1.5-flash",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
]

for m in candidate_models:
    try:
        res = client.models.generate_content(
            model=m,
            contents="Hello! Return JSON: {\"status\": \"ok\"}"
        )
        print(f"Model {m}: SUCCESS! Response: {res.text.strip()[:50]}")
    except Exception as e:
        print(f"Model {m}: FAILED ({e})")
