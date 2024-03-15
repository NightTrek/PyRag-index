import os
import time
import inspect

from ragatouille import RAGPretrainedModel
from chonk.Chonkv0 import process_pdfs_in_folder

def debug(message):
    caller = inspect.currentframe().f_back
    print(f"[DEBUG] {time.strftime('%Y-%m-%d %H:%M:%S')} - {caller.f_code.co_filename}:{caller.f_lineno} - {message}")
# Override the built-in print function
def custom_print(*args, **kwargs):
    # Convert args to a string message
    message = ' '.join(str(arg) for arg in args)
    # Call debug with this message
    debug(message)

# Assign the custom print to replace the built-in print
# builtins.print = custom_print



def create_or_load_index(index_path):
    RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    print("initializing index")
    if os.path.exists(index_path + "/arxiv-index"):
        debug("Loading existing index...")
        return RAG.from_index("arxiv-pdfs/arxiv-index")
    else:
        debug("BEGINGING DOCUMENT INDEXING...")
        # get document chunks
        # documents = process_pdfs_in_folder(index_path)
                                                    
        file_names = [f for f in os.listdir(index_path) if os.path.isfile(os.path.join(index_path, f))]                       
        return RAG.index(
            file_names,
            document_ids=file_names,
            index_name="arxiv-index",
        )




