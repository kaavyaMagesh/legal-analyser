# risk_detector.py - Identify unfair or risky terms

import google.generativeai as genai
import os
import json
from dotenv import load_dotenv
from prompts import RISK_DETECTION_PROMPT, SENTIMENT_PROMPT

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-2.5-flash-lite')

def detect_risks(chunks):
    """
    Scan document for risky terms
    
    Input: [{"text": "...", "section": "..."}, ...]
    Output: 
    {
        "warnings": ["⚠️ High late fee", "⚠️ No refund policy"],
        "risk_level": "High",
        "details": [...]
    }
    """
    try:
        combined_text = "\n\n".join([chunk["text"] for chunk in chunks])
        prompt = RISK_DETECTION_PROMPT.format(text=combined_text)
        
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # Try to parse as JSON, fallback to text
        try:
            risks = json.loads(result_text)
        except:
            # If not JSON, convert to simple format
            risks = [{"description": result_text, "severity": "Medium"}]
        
        # Create warning messages
        warnings = []
        max_severity = "Low"
        
        for risk in risks:
            severity = risk.get("severity", "Medium")
            description = risk.get("description", "Potential issue found")
            warnings.append(f"⚠️ {description}")
            
            # Track highest severity
            if severity == "High":
                max_severity = "High"
            elif severity == "Medium" and max_severity == "Low":
                max_severity = "Medium"
        
        return {
            "warnings": warnings,
            "risk_level": max_severity,
            "details": risks
        }
    
    except Exception as e:
        return {
            "warnings": [f"Error analyzing risks: {str(e)}"],
            "risk_level": "Unknown",
            "details": []
        }

def analyze_sentiment(text):
    """
    Determine if document is fair or biased
    
    Output: "Fair and Balanced" or "Contains Harsh Penalties", etc.
    """
    try:
        prompt = SENTIMENT_PROMPT.format(text=text)
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        return f"Error: {str(e)}"