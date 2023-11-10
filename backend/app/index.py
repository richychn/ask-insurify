import pinecone
from llama_index import VectorStoreIndex, StorageContext, ServiceContext
from llama_index.vector_stores import PineconeVectorStore
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.llms import LlamaCPP
from local import PINECONE_API, PINECONE_ENV

def get_index():
    model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")
    print("****** Embed Model Loaded ******")
    llm = LlamaCPP(
        model_url=model_url,
        model_path=None,
        temperature=0.1,
        max_new_tokens=256,
        context_window=3900,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": 1},
        verbose=False,
    )
    print("****** LLM Loaded ******")
    pinecone.init(api_key=PINECONE_API, environment=PINECONE_ENV)
    vector_store = PineconeVectorStore(pinecone.Index("sitemap"))
    print("****** Vector Store Loaded ******")
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)
    print("****** Index Loaded ******")
    return index