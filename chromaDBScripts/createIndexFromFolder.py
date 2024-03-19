import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
import chromadb



chroma_client = chromadb.Client()

def generate_index_from_folder(index_path, collection_name):
    db = chromadb.PersistentClient(path="./chroma_db")
    chroma_collection = db.get_or_create_collection(collection_name)
    
    # define embedding function
    embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
    
    # load documents
    reader = SimpleDirectoryReader(index_path)
    
    documents = reader.load_data(num_workers=8, show_progress=True)
    print("docs done")
    # set up ChromaVectorStore and load in data
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context, embed_model=embed_model,
        show_progress=True,
    )
    print("index cgenerated")
    return index
#     return index                

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
    response = query_engine.retrieve(query)
    return response


def query_with_ollama(query, collection_name = "mini-arxiv-pdfs"):
    llm_ollama = Ollama(model="mistral:latest", request_timeout=30.0)
    vector_index = fetch_chroma_index(collection_name)
    query_engine = vector_index.as_chat_engine(llm=llm_ollama)
    response = query_engine.retrieve(query)
    return response