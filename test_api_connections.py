import os
from dotenv import load_dotenv

load_dotenv()

print("Gemini key:", "FOUND" if os.getenv("GEMINI_API_KEY") else "MISSING")
print("Groq key:", "FOUND" if os.getenv("GROQ_API_KEY") else "MISSING")
print("Cohere key:", "FOUND" if os.getenv("COHERE_API_KEY") else "MISSING")