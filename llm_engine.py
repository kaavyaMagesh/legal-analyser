import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

# Gemini model initialization
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
LLM_MODEL = "gemini-1.5-pro-latest"


def build_prompt(user_query, chunks):
    """
    Construct a structured legal analysis prompt using retrieved RAG chunks.
    Ensures grounding and reduces hallucination.
    """
    context_text = "\n\n---\n".join([c["text"] for c in chunks])

    prompt = f"""
You are a legal assistant AI designed to simplify and explain legal documents for everyday users.

Below is extracted text from a legal document. Use ONLY this information.

================ DOCUMENT EXTRACTS ================
{context_text}
===================================================

USER QUESTION:
{user_query}

YOUR TASKS:
1. Provide a clear direct answer to the user's question.
2. Provide a short summary of the relevant text.
3. Provide a simplified explanation (as if explaining to a teenager).
4. Identify and list any legal risks, penalties, obligations, or warning signs.
5. Extract 3–6 key points as bullet points.
6. Do NOT hallucinate. If the answer is not in the extracts, say "Not available in the document."
7. Answer in structured JSON:

{{
  "answer": "...",
  "summary": "...",
  "simplified": "...",
  "risks": ["...", "..."],
  "key_points": ["...", "..."],
  "citation_chunks": [...]
}}

Generate JSON only. No extra text.
"""

    return prompt


def run_llm(user_query, chunks):
    """
    Runs Gemini on the RAG retrieved chunks and produces structured JSON output.
    """
    prompt = build_prompt(user_query, chunks)

    response = client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt,
        temperature=0.2
    )

    # Raw text from Gemini
    text_response = response.text

    # Try converting to JSON (LLM should already output structured JSON)
    try:
        import json
        result = json.loads(text_response)
    except Exception:
        # fallback if the model added stray formatting
        result = {"raw_output": text_response}

    # Add chunks used for transparency
    result["citation_chunks"] = [c["text"] for c in chunks]

    return result
