from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from utils_scraper import extract_text_from_url
from utils_embedding import chunk_text, embed_chunks, model
from rag_retriever import retrieve_top_k
from rag_generator import generate_answer_with_citations

app = FastAPI()

# Global index and chunks
chunks = []
index = None

class IndexRequest(BaseModel):
    urls: list[str]

class QueryRequest(BaseModel):
    query: str

@app.post("/api/v1/index")
def index_documents(req: IndexRequest):
    global chunks, index
    try:
        chunks = []
        for url in req.urls:
            text = extract_text_from_url(url)
            chunks.extend(chunk_text(text))
        index, _ = embed_chunks(chunks)
        return {"message": f"Indexed {len(chunks)} chunks from {len(req.urls)} URLs."}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/api/v1/chat")
def chat(req: QueryRequest):
    try:
        if not index or not chunks:
            return JSONResponse(status_code=400, content={"error": "No documents indexed yet."})
        top_chunks = retrieve_top_k(req.query, index, chunks, model)
        answer = generate_answer_with_citations(req.query, top_chunks)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})