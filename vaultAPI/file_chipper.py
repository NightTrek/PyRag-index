import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os
import time

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
    total_files = len(os.listdir(file_path))

    print(f"total files in folder: {total_files}")
    for i in range(0, total_files, batch_size):
        file_fields = []
        for file_name in os.listdir(file_path)[i:i+batch_size]:
            file_fields.append(
                ('files', (file_name, open(os.path.join(file_path, file_name), 'rb')))
            )
        multiPartForms.append(MultipartEncoder(fields=file_fields))
    # Request chunking for the split up batches of files
    print(f"chunking {len(multiPartForms)} forms")        
    results_chunks = []
    for form in multiPartForms:
        print('Next Batch')

        try:
            response = requests.post(api_url, data=form, headers={'Content-Type': form.content_type}, timeout=60)
            response.raise_for_status()
            json_results = response.json()['results']
            for chunkArray in json_results:
                results_chunks.extend([FileChipperResponse(text=result['text'], positionData=[PositionData(page_idx=pos['page_idx'], block_idx=pos['block_idx'], bbox=[int(coord) for coord in pos['bbox']], tag=pos['tag']) for pos in result['positionData']]) for result in chunkArray])

            print(f"Total_file_chunks = {len(results_chunks)}")
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