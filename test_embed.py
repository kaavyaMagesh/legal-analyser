from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
resp = client.models.embed_content(model="gemini-embedding-001", contents=["hello world"])

print("RESP TYPE:", type(resp))
print("HAS ATTR embeddings?", hasattr(resp, "embeddings"))
print("embeddings repr:", repr(getattr(resp, "embeddings", None)))
first = getattr(resp, "embeddings", None)[0]
print("first type:", type(first))
# print available attributes for inspection
print("dir(first) sample:", [a for a in dir(first) if not a.startswith("_")][:40])
# try dict-like
print("first __dict__:", getattr(first, "__dict__", None))
