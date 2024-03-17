import os
import time
import inspect
import builtins

from ragatouille import RAGPretrainedModel
from chonk.Chonkv0 import process_pdfs_in_folder

# Override the built-in print function
def custom_print(*args, **kwargs):
    # Convert args to a string message
    message = ' '.join(str(arg) for arg in args)
    caller = inspect.currentframe().f_back
    # Call debug with this message
    builtins.__print__(f"[DEBUG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {caller.f_code.co_filename}:{caller.f_lineno} - {message}")


# Assign the custom print to replace the built-in print
builtins.__print__ = builtins.print
builtins.print = custom_print


def create_or_load_index(index_path):
    RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    print("initializing index")
    if os.path.exists(os.path.join(index_path, "plan.json")):
        print("Loading existing index...")
        return RAG.from_index(index_path)
    else:
        print("BEGINGING DOCUMENT INDEXING...")
        # get document chunks
        # documents = process_pdfs_in_folder(index_path)
                                                    
        text, ids, metadatas = process_pdfs_in_folder(index_path)  

        print("PDFS PROCESSED CREATING THE INDEX")               
        return RAG.index(
            collection=text,
            document_ids=ids,
            document_metadatas=metadatas,
            index_name="arxiv-index",
        )
