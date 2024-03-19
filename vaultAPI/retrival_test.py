import os
import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import init

init.init()


api_key = os.environ["VAULT_API_KEY"]



def ask_question(question):
    url = "https://vault.pash.city/api/questions?api_key=" + api_key
    data = MultipartEncoder({
        "question": question,
        "namespace": 'mini-arxiv',
    })

    response = requests.post(url, data=data, headers={"Content-Type": data.content_type})
    return response.json()


def retrive_chunks(query):
    url = "https://vault.pash.city/api/retrieve?api_key=" + api_key
    data = {
        "queries": [query],
        "namespace": 'mini-arxiv',

    }

    response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
    return response.json()