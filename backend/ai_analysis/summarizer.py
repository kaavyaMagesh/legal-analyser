# summarizer.py - Document summarization

import google.generativeai as genai
import os
from dotenv import load_dotenv
from prompts import SUMMARIZE_PROMPT

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def summarize_document(chunks):
    """
    Takes retrieved text chunks and creates a summary
    
    Input: 
        chunks = [{"text": "...", "section": "...", "page": 3}, ...]
    
    Output:
        "Simple summary of the document in plain English"
    """
    try:
        # Combine all chunks into one text
        combined_text = "\n\n".join([chunk["text"] for chunk in chunks])
        
        # Create prompt
        prompt = SUMMARIZE_PROMPT.format(text=combined_text)
        
        # Call Gemini AI
        response = model.generate_content(prompt)
        
        return response.text.strip()
    
    except Exception as e:
        return f"Error generating summary: {str(e)}"

def summarize_section(section_text):
    """
    Summarize a specific section
    
    Input: "long legal text..."
    Output: "short summary"
    """
    try:
        prompt = SUMMARIZE_PROMPT.format(text=section_text)
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"