from vaultAPI.file_chipper import FileChipperResponse, chunk_files
from typing import List, Dict, Optional
from pydantic import BaseModel

import requests
import datetime
import os 


class MetadataItem(BaseModel):
    chunk_html: str
    content: str
    id: str
    link: str
    metadata: Dict[str, str]
    time_stamp: str
    weight: float

class ScoreChunk(BaseModel):
    metadata: List[MetadataItem]
    score: float

class TrieveSearchResponse(BaseModel):
    score_chunks: List[ScoreChunk]
    total_chunk_pages: int = 0


def upload_chunks( dataset_id, chunks: list[FileChipperResponse], api_key = os.environ['TRIVE_API_KEY']):
    url = f'https://api.trieve.ai/api/chunk'
    headers = {
        'Authorization': api_key, # Your Trieve API Key from the dashboard
        'TR-Dataset': dataset_id, # Your Dataset ID of the dataset you created in the dashboard
        'Content-Type': 'application/json'
    }
    for chunk in chunks:
        
        data = {
            'chunk_html': chunk.text, # The text content of the chunk you want indexed
            'link': "https://ntrek.dev", # The link to the chunk if it exists on the web
            'tag_set': ["arxiv", "vaultAPI"], # Tags to be associated with the chunk. You can use these tags to filter your search results
            'timestamp': datetime.now().isoformat(), # Set the timestamp to the current date and time when the script is run
            'tracking_id': "chunk1", # Any unique identifier you want to associate with the chunk to help you correlate it with your data
            'metadata': chunk.positionData.to_json(), # Any additional metadata you want to associate with the chunk
            'weight': 1 # You can use this param to give a weight to the chunk. i.e. > 1 will push it up in the results, < 1 will push it down in the results
        }
        response = requests.post(url, headers=headers, json=data)
        print(response.json())


def vault_chunk_and_upload(file_path, dataset_id = os.environ["TRIVE_DATASET_ID"]):
    print("Chunking files...")
    chunks = chunk_files(file_path)
    print(f"created {len(chunks)} chunks")
    print("Uploading chunks...")
    upload_chunks(dataset_id, chunks)
    print("Done!")


def search_chunks(
        query,
        limit=10,
        search_type="hybrid",
        api_key = os.environ['TRIVE_API_KEY'],
        dataset_id = os.environ["TRIVE_DATASET_ID"]):
    url = f'https://api.trieve.ai/api/chunk/search'
    headers = {
        'Authorization': api_key,
        'TR-Dataset': dataset_id,
        'Content-Type': 'application/json'
    }
    data = {
        'query': query,
        'search_type': search_type, # You can use this param to specify the search type. The options are "fulltext", "semantic", and "hybrid".
        'limit': limit, # You can use this param to specify the number of results you want to get back
        'page': 1, # You can use this param to specify the page number of the results
        'date_bias': False, # You can use this param to specify if you want to bias the results based on the timestamp of the chunks
        'use_weights': False, # You can use this param to specify if you want to use the weights of the chunks in the search results
        'filters': {
            "must": [ # All the must filters are combined using AND and have to match for the result to be returned
                #{"field": "tag_set", "match": ["Tag you want to filter by"]} # use match for text metadata fields
            ],
            "must_not": [ # All the must_not filters are combined using AND and have to NOT match for the result to be returned
                # {"field": "timestamp", "range": {
                #     "gte": 1000043043044, # use range for numerical metadata fields (timestamp is stored as a unix timestamp)
                #     "lte": 1200030030000 
                # }} # use metdata
            ],
            "should": [ # All the should filters are combined using OR and at least one of them has to match for the result to be returned
                # {"field": "metadata.key", "match": "value"} # use metadata.field to filter based on fields within your metadata JSON object
            ]
        }
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        return TrieveSearchResponse(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while making the request: {e}")
        return None
    except ValueError as e:
        print(f"Error occurred while parsing the JSON response: {e}")
        return None
