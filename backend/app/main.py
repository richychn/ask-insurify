from fastapi import FastAPI
from pydantic import BaseModel
from app.index import get_index


class Query(BaseModel):
    question: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/ask")
async def ask(query: Query):
    index = get_index()
    query_engine = index.as_query_engine()
    response = query_engine.query(query.question)
    sources = list({v['Source'] for v in response.metadata.values()})
    return {
        "response": response.response,
        "sources": sources
    }