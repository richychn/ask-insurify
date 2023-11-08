from fastapi import FastAPI
from pydantic import BaseModel
from index.index_fetcher import IndexFetcher
from index.db import table_exists

class Query(BaseModel):
    url: str
    question: str

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/ask")
async def ask(query: Query):
    is_data_loaded = table_exists(query.url)
    index = IndexFetcher(url=query.url, is_data_loaded=is_data_loaded).index
    query_engine = index.as_query_engine()
    response = query_engine.query(query.question)
    sources = list({v['Source'] for v in response.metadata.values()})
    return {
        "response": response.response,
        "sources": sources
    }