# main.py - API endpoints for your team

from flask import Flask, request, jsonify
from flask_cors import CORS
from summarizer import summarize_document, summarize_section
from simplifier import simplify_clause, simplify_multiple_sections
from risk_detector import detect_risks, analyze_sentiment
from qa_handler import answer_question, explain_jargon

app = Flask(__name__)
CORS(app)  # Allow frontend to call these APIs

@app.route('/api/health', methods=['GET'])
def health_check():
    """Test if API is working"""
    return jsonify({"status": "AI Analysis API is running!"})

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """
    Endpoint for document summarization
    
    Expected Input:
    {
        "chunks": [
            {"text": "...", "section": "Payment", "page": 2},
            {"text": "...", "section": "Penalties", "page": 3}
        ]
    }
    """
    data = request.json
    chunks = data.get('chunks', [])
    
    if not chunks:
        return jsonify({"error": "No chunks provided"}), 400
    
    summary = summarize_document(chunks)
    
    return jsonify({
        "summary": summary,
        "chunk_count": len(chunks)
    })

@app.route('/api/simplify', methods=['POST'])
def simplify():
    """
    Simplify legal text
    
    Input: {"text": "The Lessee shall..."}
    """
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    simplified = simplify_clause(text)
    
    return jsonify({"simplified_text": simplified})

@app.route('/api/analyze-risks', methods=['POST'])
def analyze_risks():
    """
    Detect risky terms
    
    Input: {"chunks": [...]}
    """
    data = request.json
    chunks = data.get('chunks', [])
    
    if not chunks:
        return jsonify({"error": "No chunks provided"}), 400
    
    risks = detect_risks(chunks)
    
    # Also get sentiment
    combined_text = "\n".join([c["text"] for c in chunks])
    sentiment = analyze_sentiment(combined_text)
    
    return jsonify({
        "warnings": risks["warnings"],
        "risk_level": risks["risk_level"],
        "sentiment": sentiment,
        "details": risks["details"]
    })

@app.route('/api/qa', methods=['POST'])
def qa():
    """
    Answer questions
    
    Input: 
    {
        "question": "What is the late fee?",
        "context_chunks": [...]
    }
    """
    data = request.json
    question = data.get('question', '')
    context_chunks = data.get('context_chunks', [])
    
    if not question:
        return jsonify({"error": "No question provided"}), 400
    
    answer = answer_question(question, context_chunks)
    
    return jsonify({"answer": answer})

@app.route('/api/explain-jargon', methods=['POST'])
def jargon():
    """
    Explain legal terms
    
    Input: {"text": "..."}
    """
    data = request.json
    text = data.get('text', '')
    
    if not text:
        return jsonify({"error": "No text provided"}), 400
    
    explanations = explain_jargon(text)
    
    return jsonify({"jargon_explained": explanations})

@app.route('/api/full-analysis', methods=['POST'])
def full_analysis():
    """
    Complete analysis - all features in one call
    
    Input:
    {
        "chunks": [...],
        "question": "..." (optional)
    }
    """
    data = request.json
    chunks = data.get('chunks', [])
    question = data.get('question', None)
    
    if not chunks:
        return jsonify({"error": "No chunks provided"}), 400
    
    # Run all analyses
    summary = summarize_document(chunks)
    risks = detect_risks(chunks)
    combined_text = "\n".join([c["text"] for c in chunks])
    sentiment = analyze_sentiment(combined_text)
    jargon = explain_jargon(combined_text)
    
    result = {
        "summary": summary,
        "warnings": risks["warnings"],
        "risk_level": risks["risk_level"],
        "sentiment": sentiment,
        "jargon_explained": jargon
    }
    
    # If question provided, answer it
    if question:
        result["qa_answer"] = answer_question(question, chunks)
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)