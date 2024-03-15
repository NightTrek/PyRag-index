import os
import time
import inspect
from concurrent.futures import ThreadPoolExecutor

from ragatouille import RAGPretrainedModel
from llama_index import SimpleDirectoryReader
import PyPDF2
import tiktoken

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


def watch_for_commands():
    debug("Watching for commands. Type '/exit' to stop.")
    try:
        while True:
            message = input()
            if message.startswith("/"):
                if message == "/exit":
                    debug("Exiting command watch.")
                    break
                else:
                    debug(f"Command received: {message}")
            else:
                debug("Not a command. Ignoring.")
    except KeyboardInterrupt:
        debug("\nInterrupted by user. Exiting.")

if __name__ == "__main__":
    RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    watch_for_commands()

def create_or_load_index(index_path):
    RAG = RAGPretrainedModel.from_pretrained("colbert-ir/colbertv2.0")
    if os.path.exists(index_path + "/arxiv-index"):
        debug("Loading existing index...")
        RAG.from_index("arxiv-pdfs/arxiv-index")
    else:
        debug("BEGINGING DOCUMENT INDEXING...")
        # get document chunks
        documents = process_pdfs_in_folder(index_path)
        RAG.index(
            documents
        )



def process_pdfs_in_folder(folder, worker_threads=12):
    pdf_files = [file for file in os.listdir(folder) if file.endswith(".pdf")]
    
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder, pdf_file)
            future = executor.submit(process_pdf, pdf_path)
            futures.append(future)
        
        text_chunks = []
        for future in futures:
            text_chunks.extend(future.result())
    
    return text_chunks

def process_pdf(pdf_path):
    text, title = PDF_to_text(pdf_path)
    chunks = Chunk_text(text)
    document_id = os.path.basename(pdf_path).rstrip(".pdf")
    metadata = {"title": title}
    return chunks, document_id, metadata

def PDF_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        title = ""
        for page in reader.pages:
            text += page.extract_text()
            if not title:
                title_match = reader.search(r'(?i)^(title|h1):\s*(.+)$', text, reader.MULTILINE)
                if title_match:
                    title = title_match.group(2)
    return text, title


# uses an LLM text chunking algorithm to divide a large text into chunks of a fixed size tokens (default 256) 
def Chunk_text(text, chunk_size=256):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size):
        chunk = encoding.decode(tokens[i:i+chunk_size])
        chunks.append(chunk)
    return chunks

