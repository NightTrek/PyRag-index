import PyPDF2
import tiktoken
from concurrent.futures import ThreadPoolExecutor
import os
import re

def process_pdfs_in_folder(folder, worker_threads=12):
    pdf_files = [file for file in os.listdir(folder) if file.endswith(".pdf")]
    
    with ThreadPoolExecutor(max_workers=worker_threads) as executor:
        futures = []
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder, pdf_file)
            future = executor.submit(process_pdf, pdf_path)
            futures.append(future)
        
        documents_list = []
        doc_id_list = []
        metadata_list = []
        for future in futures:
            text, document_id, metadata = future.result()
            documents_list.append(text)
            doc_id_list.append(document_id)
            metadata_list.append(metadata)
    
    return documents_list, doc_id_list, metadata_list

def process_pdf(pdf_path):
    text, title = PDF_to_text(pdf_path)
    # chunks = Chunk_text(text)
    document_id = os.path.basename(pdf_path).rstrip(".pdf")
    metadata = {"title": title}
    return text, document_id, metadata

def PDF_to_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        title = ""
        for page in reader.pages:
            text += page.extract_text()
            if not title:
                title_match = re.search(r'(?i)^(title|h1):\s*(.+)', text, re.MULTILINE)
                if title_match:
                    title = title_match.group(2)
    return text, title

def Chunk_text(text, chunk_size=256):
    encoding = tiktoken.get_encoding("cl100k_base")
    tokens = encoding.encode(text)
    chunks = []
    start_idx = 0
    while start_idx < len(tokens):
        end_idx = min(start_idx + chunk_size, len(tokens))
        if end_idx < len(tokens):
            # Find the nearest end of sentence or paragraph within a certain tolerance
            tolerance = chunk_size // 10
            while end_idx < len(tokens) and tokens[end_idx] not in {encoding.encode('.')[0], encoding.encode('!')[0], encoding.encode('?')[0], encoding.encode('\n')[0]} and end_idx - start_idx < chunk_size + tolerance:
                end_idx += 1
        chunk_tokens = tokens[start_idx:end_idx]
        chunk = encoding.decode(chunk_tokens)
        chunks.append(chunk)
        start_idx = end_idx
    return chunks
