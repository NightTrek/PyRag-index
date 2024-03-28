
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import init
from trieve.TrieveTools import vault_chunk_and_upload
from vaultAPI.createIndex import create_index_from_folder

init.init()

path_to_pdfs = 'mini-arxiv-pdfs/'

print("============ creating Trieve Index ============")
vault_chunk_and_upload(path_to_pdfs)

# print("============ creating Vault Index ============")
# create_index_from_folder(path_to_pdfs)

print("============ Completed ============")