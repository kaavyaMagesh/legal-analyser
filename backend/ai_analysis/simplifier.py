# simplifier.py - Simplify complex clauses

import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import SIMPLIFY_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def simplify_clause(legal_text):
    """
    Convert complex legal language to simple English
    
    Input: "The Lessee shall indemnify the Lessor..."
    Output: "You must protect the landlord from any legal claims..."
    """
    try:
        prompt = SIMPLIFY_PROMPT.format(clause=legal_text)
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"

def simplify_multiple_sections(sections_dict):
    """
    Simplify multiple sections at once
    
    Input: {"Payment Terms": "The Lessee shall...", "Penalties": "..."}
    Output: {"Payment Terms": "Simple version", "Penalties": "Simple version"}
    """
    simplified = {}
    
    for section_name, section_text in sections_dict.items():
        simplified[section_name] = simplify_clause(section_text)
    
    return simplified