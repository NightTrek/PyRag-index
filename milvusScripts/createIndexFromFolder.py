import openai

from pymilvus import connections, db
from chonk.Chonkv0 import process_pdfs_in_folder

connection = connections.connect(
  alias="default",
  uri="localhost:19530",
  token="root:Milvus",
)




def generate_index_from_folder(index_path):
    text, ids, metadatas = process_pdfs_in_folder(index_path)
    print("PDFS PROCESSED CREATING THE INDEX")
    database = db.using_database("default")






generate_index_from_folder("mini-arxiv-pdfs")

connections.disconnect("default")

