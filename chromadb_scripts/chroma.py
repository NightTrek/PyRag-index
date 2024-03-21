import chromadb
from llama_index.core import VectorStoreIndex
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama

from pydantic.v1.error_wrappers import ValidationError
import chromadb



chroma_client = chromadb.Client()

def fetch_chroma_index(collection_name):
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection(collection_name)
    embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    index = VectorStoreIndex.from_vector_store(
        vector_store,
        embed_model=embed_model,
    )
    print("index found")
    return index


def query_chroma(query, collection_name = "mini-arxiv-pdfs"):
    vector_index = fetch_chroma_index(collection_name)
    query_engine = vector_index.as_retriever()
    try:
        results = query_engine.retrieve(query)
        return [result.text for result in results]
    except (AttributeError, ValidationError) as e:
        print(f"Error retrieving results: {str(e)}")
        return []


def query_with_ollama(query, collection_name = "mini-arxiv-pdfs"):
    llm_ollama = Ollama(model="mistral:latest", request_timeout=30.0)
    vector_index = fetch_chroma_index(collection_name)
    query_engine = vector_index.as_chat_engine(llm=llm_ollama)
    response = query_engine.retrieve(query)
    return response