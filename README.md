# Legal Analyser  
### *Deciphering the Law with Intelligence*

**Legal Analyser** is an advanced NLP-powered platform that automatically **summarizes legal documents**, **detects high-risk clauses**, and **translates complex legal language into plain English**—making contracts accessible to non-lawyers.

---

## About The Project

Legal documents are often dense, verbose, and difficult for non-legal professionals to interpret. **Legal Analyser** bridges this gap using **state-of-the-art Natural Language Processing (NLP)** techniques.

By uploading a legal document (PDF or DOCX), users receive an instant, structured analysis that:
- Breaks down the document into logical sections
- Highlights risky clauses and liabilities
- Generates concise, abstractive summaries
- Simplifies complex legal jargon into understandable language

---

## Key Features

### Intelligent Parsing
- OCR-enabled ingestion of scanned PDFs and Word documents  
- Supports both digital and scanned contracts  

### Abstractive Summarization
- Uses fine-tuned Transformer models (e.g., **BART-Large-CNN**)  
- Generates concise summaries for long clauses and sections  

### Risk Detection
- Automatically flags high-risk clauses such as:
  - Indemnity
  - Termination at Will
  - Non-Compete
  - Liability clauses  

### Named Entity Recognition (NER)
- Extracts and tabulates:
  - Parties involved
  - Dates
  - Jurisdictions
  - Monetary values  

### Simplification Engine
- **“Translate to Simple English”** feature  
- Converts complex legalese into plain, readable language  

---

## System Architecture

The application follows a **decoupled client–server architecture**, separating ML-heavy processing from UI rendering.

### Ingestion
- User uploads a document (PDF/DOCX)
- Text extraction via **PyPDF2** or **Tesseract OCR**

### Preprocessing
- Text cleaning and normalization
- Tokenization and clause segmentation

### Inference Pipeline
- **NER Model (spaCy)** – Entity extraction  
- **Clause Classification (BERT)** – Clause type detection  
- **Summarization (Hugging Face Transformers)** – Abstractive summaries  

### Response
- Structured JSON sent to frontend
- Interactive rendering and visualization

---

## Tech Stack

### Backend (AI & API)
- **Language:** Python 3.9  
- **Framework:** Flask (REST API)  
- **ML Libraries:**  
  - PyTorch  
  - Hugging Face Transformers  
  - spaCy  
  - Scikit-learn  
- **OCR:** Tesseract, pdf2image  
- **Database:** MongoDB (document metadata & user logs)

---

### Frontend (UI/UX)
- **Framework:** React.js (Vite)  
- **State Management:** Redux Toolkit  
- **Styling:** Tailwind CSS + Headless UI  
- **Visualization:** Chart.js (risk distribution & analytics)
