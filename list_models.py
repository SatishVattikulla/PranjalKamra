import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

try:
    models = client.models.list()
    print("Available models:")
    for m in models:
        print(f"- {m.name} (Supported actions: {getattr(m, 'supported_generation_methods', getattr(m, 'supported_actions', ''))})")
except Exception as e:
    print("Error listing models:", e)
