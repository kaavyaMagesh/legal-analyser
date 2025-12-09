import os
from dotenv import load_dotenv
from google import genai
from pinecone import Pinecone

load_dotenv()

# ============================================================
# GEMINI EMBEDDING SETUP (3072-dim)
# ============================================================
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
EMBED_MODEL = "gemini-embedding-001"


# ---- Robust embedding extraction ----
def _extract_vector(emb_obj):
    """
    Extract embedding vector from the different possible shapes
    Google GenAI may return.
    """
    if isinstance(emb_obj, dict):
        for k in ("embedding", "value", "values", "vector"):
            if k in emb_obj:
                return emb_obj[k]

    for attr in ("embedding", "value", "values", "vector"):
        if hasattr(emb_obj, attr):
            val = getattr(emb_obj, attr)
            if isinstance(val, (list, tuple)):
                return list(val)
            if isinstance(val, dict):
                for k in ("embedding", "values", "vector"):
                    if k in val:
                        return val[k]

    raise RuntimeError(
        f"Cannot extract embedding vector from object: {emb_obj}"
    )


def embed_text(text: str):
    resp = client.models.embed_content(
        model=EMBED_MODEL,
        contents=[text]
    )
    emb_list = getattr(resp, "embeddings", None)
    if emb_list is None:
        raise RuntimeError("No embeddings returned from Gemini")
    return _extract_vector(emb_list[0])


# ============================================================
# PINECONE v8 SETUP (MUST USE 3072 DIMENSION)
# ============================================================

pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
# pc.delete_index("pineindex1")

index_name = os.getenv("PINECONE_INDEX_NAME")

region = os.getenv("PINECONE_ENV")

# pc.create_index(
#     name=index_name,
#     dimension=3072,    # IMPORTANT
#     metric="cosine",
#     spec={
#         "serverless": {"cloud": "aws", "region": region}
#     }
# )


existing_indexes = [idx.name for idx in pc.list_indexes()]

# Re-create the index if missing (dimension MUST be 3072)
if index_name not in existing_indexes:
    pc.create_index(
        name=index_name,
        dimension=3072,   # IMPORTANT
        metric="cosine",
        spec={
            "serverless": {
                "cloud": "aws",
                "region": region
            }
        }
    )

# Connect to index
index = pc.Index(index_name)


# ============================================================
# STORE CHUNKS
# ============================================================
def store_chunks_in_pinecone(chunks, doc_id: str):

    vectors = []
    for i, chunk in enumerate(chunks):
        emb = embed_text(chunk)

        vectors.append({
            "id": f"{doc_id}-{i}",
            "values": emb,
            "metadata": {
                "text": chunk,
                "chunk_index": i,
                "doc_id": doc_id
            }
        })

    index.upsert(vectors=vectors)

    return {"stored_vectors": len(vectors)}


# ============================================================
# RETRIEVAL (RAG)
# ============================================================
def retrieve_relevant_chunks(query: str, top_k: int = 5):

    query_vector = embed_text(query)

    results = index.query(
        vector=query_vector,
        top_k=top_k,
        include_metadata=True
    )

    output = []
    for match in results["matches"]:
        output.append({
            "text": match["metadata"]["text"],
            "score": match["score"]
        })

    return output


# SAMPLE QUERY
# {
#   "query": "What is this document about?"
# }

# EXAMPLE OUTPUT
# {
#   "top_chunks": [
#     {
#       "text": "This agreement is made between the landlord and the tenant...",
#       "score": 0.88
#     },
#     {
#       "text": "The tenant agrees to pay rent on the first of every month...",
#       "score": 0.83
#     }
#   ]
# }