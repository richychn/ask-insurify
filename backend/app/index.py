import pinecone
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.vector_stores import PineconeVectorStore
from llama_index.embeddings import HuggingFaceEmbedding
from transformers import AutoModel, AutoTokenizer
from llama_index.llms import LlamaCPP
from local import PINECONE_API, PINECONE_ENV
from os import getcwd
import sys

def get_index():
    # model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"
    dir = getcwd()
    model_path = f"{dir}/app/weights/llama-2-13b-chat.Q4_0.gguf"
    embedding_model = AutoModel.from_pretrained(pretrained_model_name_or_path=f'{dir}/app/weights/embed_model/')
    embedding_tokenizer = AutoTokenizer.from_pretrained(pretrained_model_name_or_path=f'{dir}/app/weights/embed_tokenizer/')
    embed_model = HuggingFaceEmbedding(model=embedding_model, tokenizer=embedding_tokenizer)
    print("****** Embed Model Loaded ******")
    llm = LlamaCPP(
        model_url=None,
        model_path=model_path,
        temperature=0.1,
        max_new_tokens=256,
        context_window=3900,
        generate_kwargs={},
        model_kwargs={"n_gpu_layers": 1},
        verbose=False,
    )
    print("****** LLM Loaded ******")
    sys.stdout.flush()
    pinecone.init(api_key=PINECONE_API, environment=PINECONE_ENV)
    vector_store = PineconeVectorStore(pinecone.Index("sitemap"))
    print("****** Vector Store Loaded ******")
    sys.stdout.flush()
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store, service_context=service_context)
    print("****** Index Loaded ******")
    sys.stdout.flush()
    return index