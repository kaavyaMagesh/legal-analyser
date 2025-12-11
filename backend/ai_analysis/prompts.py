# prompts.py - All AI prompt templates

SUMMARIZE_PROMPT = """
You are a legal document expert. Summarize the following legal text in simple, clear language that anyone can understand.

Legal Text:
{text}

Provide a concise summary in 3-5 sentences. Focus on the main points and obligations.
"""

SIMPLIFY_PROMPT = """
You are a legal translator. Convert this complex legal clause into plain English.

Legal Clause:
{clause}

Rewrite this in simple terms that a 10th grader would understand. Keep it short and clear.
"""

RISK_DETECTION_PROMPT = """
You are a legal analyst. Analyze the following document sections and identify any risky, unfair, or concerning terms.

Document Sections:
{text}

List all potential risks, penalties, or unfavorable terms. For each risk:
- Describe the risk clearly
- Explain why it's concerning
- Rate severity as: Low, Medium, or High

Return your analysis as a JSON array of risks.
"""

QA_PROMPT = """
You are a helpful legal assistant. Answer the user's question based ONLY on the provided context.

Context:
{context}

User Question: {question}

Provide a clear, direct answer. If the answer is not in the context, say "I cannot find this information in the document."
"""

JARGON_PROMPT = """
Identify all legal jargon and technical terms in the following text and explain them in simple language.

Text:
{text}

Return a JSON object where keys are the jargon terms and values are simple explanations.
Example: {{"tenant": "The person renting the property", "indemnify": "To protect someone from legal responsibility"}}
"""

SENTIMENT_PROMPT = """
Analyze the tone and fairness of this legal document.

Document Text:
{text}

Rate the document's sentiment as one of:
- Fair and Balanced
- Slightly Favorable to One Party
- Heavily Biased
- Contains Harsh Penalties

Explain your rating in 2-3 sentences.
"""