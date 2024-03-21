import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, SummaryExtractor, QuestionsAnsweredExtractor
from llama_index.core.base.llms.types import ChatMessage, MessageRole
import chromadb
import json



chroma_client = chromadb.Client()

def generate_index_from_folder(index_path, collection_name, override=False):
    db = chromadb.PersistentClient(path="./chroma_db")
    if override:
        try:
            db.delete_collection(collection_name)
        except ValueError:
            pass
        chroma_collection = db.get_or_create_collection(collection_name)
    else:
        chroma_collection = db.get_or_create_collection(collection_name)
    
    # define embedding function
    embed_model = OllamaEmbedding(model_name="nomic-embed-text:latest")
    #llm 

    # load documents
    reader = SimpleDirectoryReader(index_path)
    
    documents = reader.load_data(num_workers=12, show_progress=True)
    print("docs done")
    # set up ChromaVectorStore and load in data
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        embed_model=embed_model,
        show_progress=True,
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=32 ),
            # TitleExtractor(llm=Ollama(model="mistral")),
            # SummaryExtractor(llm=Ollama(model="yarn-mistral", context_window=(1024*16)), num_sentences=5),
            # QuestionsAnsweredExtractor(llm=Ollama(model="yarn-mistral", context_window=(1024*16))),
            OllamaEmbedding(model_name="nomic-embed-text:latest")
        ]
    )
    print("index generated Wohoo")
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
    llm_ollama = Ollama(model="mistral", request_timeout=30.0)
    queries = llm_ollama.chat([
            ChatMessage(role=MessageRole.USER, content="Given the following prompt generate at least 3 new queries  (max 5) which can be used to help answer the input prompt. INPUT: " + query +  "|| Fromat the output into a single json object containing a results array which has the generated queries in the array")
        ])
    new_queries = json.loads(queries.message.content)['queries']
    new_queries = [q['query'] for q in new_queries]
    print(new_queries)

    vector_index = fetch_chroma_index(collection_name)
    query_engine = vector_index.as_retriever()
    response = []
    for q in new_queries:
        response.extend(query_engine.retrieve(q))
    return response


def query_with_ollama(query, collection_name = "mini-arxiv-pdfs"):
    llm_ollama = Ollama(model="mistral:latest", request_timeout=30.0)
    vector_index = fetch_chroma_index(collection_name)
    query_engine = vector_index.as_chat_engine(llm=llm_ollama)
    response = query_engine.retrieve(query)
    return response