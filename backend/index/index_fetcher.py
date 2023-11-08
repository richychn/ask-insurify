from llama_index.llms import LlamaCPP
from llama_index import StorageContext, ServiceContext, download_loader
from llama_index.vector_stores import PGVectorStore
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.embeddings import HuggingFaceEmbedding
from sqlalchemy import make_url
from local import PG_URL
import nest_asyncio
nest_asyncio.apply()


class IndexFetcher:
    def __init__(self, url, is_data_loaded, loader_name="AsyncWebPageReader"):
        self.url = url
        self.is_data_loaded = is_data_loaded
        self.loader_name = loader_name

        self.vector_store = self.make_vector_store(url)
        self.model_url = "https://huggingface.co/TheBloke/Llama-2-13B-chat-GGUF/resolve/main/llama-2-13b-chat.Q4_0.gguf"
        self.service_context = None
        self.storage_context = None
        self.index = None

        self.get_index()

    def make_vector_store(self, table_name):
        db_name = "sitemap"
        url = make_url(PG_URL)
        vector_store = PGVectorStore.from_params(
            database=db_name,
            host=url.host,
            password=url.password,
            port="5432",
            user=url.username,
            table_name=table_name,
            embed_dim=384,  # openai embedding dimension
        )
        return vector_store

    def get_llm(self):
        llm = LlamaCPP(
            # You can pass in the URL to a GGML model to download it automatically
            model_url=self.model_url,
            # optionally, you can set the path to a pre-downloaded model instead of model_url
            model_path=None,
            temperature=0.1,
            max_new_tokens=256,
            # llama2 has a context window of 4096 tokens, but we set it lower to allow for some wiggle room
            context_window=3900,
            # kwargs to pass to __call__()
            generate_kwargs={},
            # kwargs to pass to __init__()
            # set to at least 1 to use GPU
            model_kwargs={"n_gpu_layers": 1},
            verbose=True,
        )
        return llm

    def get_contexts(self):
        llm = self.get_llm()
        embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

        self.service_context = ServiceContext.from_defaults(
            llm=llm, embed_model=embed_model
        )
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

    def get_index(self):
        self.get_contexts()
        if self.is_data_loaded:
            self.index = VectorStoreIndex.from_vector_store(
                vector_store=self.vector_store,
                service_context=self.service_context
            )
        else:
            loader = download_loader(self.loader_name)()
            documents = loader.load_data(urls=[self.url])
            self.index = VectorStoreIndex.from_documents(
                documents, storage_context=self.storage_context, service_context=self.service_context
            )
