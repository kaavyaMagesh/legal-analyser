Legal Analyser 
Deciphering the Law with Intelligence.

An advanced NLP platform that automatically summarizes legal documents, detects high-risk clauses, and simplifies complex legalese into plain English.

 About The Project
Legal documents are often dense, verbose, and difficult for non-lawyers to understand. Legal Analyser bridges this gap using State-of-the-art Natural Language Processing (NLP).

By uploading a contract (PDF or DOCX), users receive an instant analysis that breaks down the document's structure, highlights liabilities, and provides abstractive summaries of key sections.

 Key Features
 Intelligent Parsing: OCR-enabled ingestion of scanned PDFs and Word documents.

 Abstractive Summarization: Uses fine-tuned Transformer models (e.g., BART-Large-CNN) to generate concise summaries of long clauses.

Risk Detection: automatically flags high-risk clauses such as Indemnity, Termination at Will, and Non-Compete agreements.

Entity Recognition (NER): Extracts and tabulates involved parties, dates, jurisdictions, and monetary amounts.

Simplification Engine: "Translate to Simple English" feature for complex legal jargon.

 System Architecture
The application follows a decoupled client-server architecture. The heavy ML lifting is done by a Python/Flask backend, while the interactive visualization is handled by a React frontend.

Ingestion: Document is uploaded and converted to raw text via PyPDF2 or Tesseract.

Preprocessing: Text is cleaned, tokenized, and split into clauses.

Inference:

NER Model (spaCy): Extracts entities.

Classification Model (BERT): Categorizes clauses (e.g., "Liability").

Summarization Model (Hugging Face): Generates summaries.

Response: JSON data is sent to the React frontend for rendering.

Tech Stack
Backend (AI & API)
Language: Python 3.9

Framework: Flask (REST API)

ML Libraries: PyTorch, Transformers (Hugging Face), spaCy, Scikit-learn

OCR: Tesseract / pdf2image

Database: MongoDB (for storing document metadata and user logs)

Frontend (UI/UX)
Framework: React.js (Vite)

State Management: Redux Toolkit

Styling: Tailwind CSS + Headless UI

Visualization: Chart.js (for risk distribution graphs)
