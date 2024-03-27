import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

api_url = "https://filechipper.com/upload"

from pydantic import BaseModel


class PositionData(BaseModel):
    page_idx: int
    block_idx: int
    bbox: list[int]
    tag: str

    def to_json(self):
        return {
            "page_idx": self.page_idx,
            "block_idx": self.block_idx,
            "bbox": self.bbox,
            "tag": self.tag
        }

class FileChipperResponse(BaseModel):
    text: str
    positionData: list[PositionData]

def chunk_files(file_path: str, batch_size: int = 4):

    multiPartForms = []
    file_fields = []
    for file_name in os.listdir(file_path):
        file_fields.append(
            ('files', (file_name, open(os.path.join(file_path, file_name), 'rb')))
        )
        if len(file_fields) > batch_size:
            multiPartForms.append(MultipartEncoder(fields=file_fields))
            file_fields = []
    # Request chunking for the split up batches of files        
    results_chunks = [FileChipperResponse]
    for form in multiPartForms:
        try:
            response = requests.post(api_url, data=form, headers={'Content-Type': form.content_type}, timeout=60)
            response.raise_for_status()
            json_results = response.json()
            results_chunks.extend(json_results.results)
        except requests.exceptions.Timeout:
            print("Request timed out. Retrying...")
            continue
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print("Rate limit exceeded. Waiting before retrying...")
                time.sleep(60)
                continue
            else:
                print(f"HTTP error occurred: {e}")
                break
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            break

    return results_chunks