import PyPDF2
import tiktoken
from concurrent.futures import ThreadPoolExecutor
import os

def process_pdfs_in_folder(folder, worker_threads=12):
    pdf_files = [file for file in os.listdir(folder) if file.endswith(".pdf")]
    
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder, pdf_file)
            future = executor.submit(process_pdf, pdf_path)
            futures.append(future)
        
        text_chunks = []
        doc_id_list = []
        for future in futures:
            chunks, document_id, metadata = future.result()
            doc_id_list.extend([document_id] * len(chunks))
                                                                                                        
            text_chunks.extend(chunks)
    
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

