from init import init
import requests
import os

init()

api_key = os.environ['VAULT_API_KEY']
url = f"https://vault.pash.city/api/get/uploads?api_key={api_key}"

response = requests.get(url)
file_list = response.json()

remove_list = []
for file in file_list:
    remove_list.append(file.id)


url = "https://vault.pash.city/api/delete/files?api_key=" + api_key
data = {
    "file_ids": remove_list
}

response = requests.post(url, json=data, headers={"Content-Type": "application/json"})
print(response.json())