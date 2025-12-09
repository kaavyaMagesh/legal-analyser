from fastapi import FastAPI, UploadFile, File
from phase1_ingestion import process_document
from rag_engine import store_chunks_in_pinecone, retrieve_relevant_chunks
import uuid

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Backend running"}


@app.post("/process")
async def process_doc(file: UploadFile = File(...)):
    return await process_document(file)


@app.post("/ingest")
async def ingest_doc(file: UploadFile = File(...)):
    processed = await process_document(file)
    chunks = processed["content_groups"]

    doc_id = str(uuid.uuid4())
    result = store_chunks_in_pinecone(chunks, doc_id)

    return {
        "doc_id": doc_id,
        "stored_chunks": result["stored_vectors"]
    }


@app.post("/query")
async def query_rag(payload: dict):
    return {
        "top_chunks": retrieve_relevant_chunks(payload["query"])
    }
