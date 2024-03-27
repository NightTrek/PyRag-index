import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import init
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder


init.init()

def create_index_from_folder(folder_path: str):
    api_key = os.environ["VAULT_API_KEY"]
    url = "https://vault.pash.city/upload?api_key=" + api_key

    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            file_path = os.path.join(folder_path, filename)
            fields = [
                ('files', (filename, open(file_path, 'rb'), 'application/pdf')),
                ('namespace', 'mini-arxiv')
            ]

            multipart_data = MultipartEncoder(fields=fields)
            print(f"MULTI PART FORM CREATED FOR {filename}")

            response = requests.post(url, data=multipart_data, headers={"Content-Type": multipart_data.content_type})
            print(f"RESPONSE RECEIVED FOR {filename}")
            try:
                print(response.json())
            except requests.exceptions.JSONDecodeError as e:
                print(f"Error decoding JSON response for {filename}: {e}")
                print(f"Response content for {filename}: {response.text}")
