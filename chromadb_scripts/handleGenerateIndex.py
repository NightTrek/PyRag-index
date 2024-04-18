import sys
import chromadb
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import TitleExtractor, SummaryExtractor, QuestionsAnsweredExtractor
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from pydantic.v1.error_wrappers import ValidationError
import chromadb
import json

EMBEDDING_MODEL = "mxbai-embed-large:latest"
# EMBEDDING_MODEL = "nomic-embed-text:latest"

# this function needs to run in main otherwise it will fail
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
    embed_model = OllamaEmbedding(model_name=EMBEDDING_MODEL)
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
            OllamaEmbedding(model_name=EMBEDDING_MODEL)
        ]
    )
    print("Completed Index Generation: " + collection_name)
    return index
#     return index                



def main():
    if len(sys.argv) < 2:
        print("Please provide the directory as a command-line argument using --path and the collection name using --name.")
        sys.exit(1)
    directory = None
    collection_name = None
    for i in range(1, len(sys.argv), 2):
        if sys.argv[i] == "--path":
            directory = sys.argv[i+1]
        elif sys.argv[i] == "--name":
            collection_name = sys.argv[i+1]
    if directory is None or collection_name is None:
        print("Please provide both --path and --name arguments.")
        sys.exit(1)
    generate_index_from_folder(directory, collection_name, override=True)

if __name__ == '__main__':
    main()