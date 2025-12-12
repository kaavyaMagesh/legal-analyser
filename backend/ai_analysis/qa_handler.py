# qa_handler.py - Answer user questions

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from prompts import QA_PROMPT, JARGON_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def answer_question(question, context_chunks):
    """
    Answer user's question using document context
    
    Input:
        question = "What is the late fee?"
        context_chunks = [{"text": "...", "score": 0.9}, ...]
    
    Output: "The late fee is 5% of the rent amount."
    """
    try:
        # Combine context
        context = "\n\n".join([chunk["text"] for chunk in context_chunks])
        
        prompt = QA_PROMPT.format(context=context, question=question)
        response = model.generate_content(prompt)
        
        return response.text.strip()
    
    except Exception as e:
        return f"Error answering question: {str(e)}"

def explain_jargon(text):
    """
    Find legal terms and explain them
    
    Input: "The lessee shall indemnify..."
    Output: {"lessee": "The person renting", "indemnify": "Protect from legal claims"}
    """
    try:
        prompt = JARGON_PROMPT.format(text=text)
        response = model.generate_content(prompt)
        
        # Try to parse as JSON
        result = response.text.strip()
        
        # Remove markdown code blocks if present
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
            result = result.strip()
        
        jargon_dict = json.loads(result)
        return jargon_dict
    
    except Exception as e:
        return {"error": f"Could not extract jargon: {str(e)}"}