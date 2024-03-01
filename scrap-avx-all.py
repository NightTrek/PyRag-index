import os
import time
import requests
import random
from bs4 import BeautifulSoup

def download_pdf(pdf_url, pdf_path, pdf_name):
    max_attempts = 5
    attempt = 0
    while attempt < max_attempts:
        try:
            response = requests.get(pdf_url)
            if response.status_code == 429:
                print("Rate limited. Waiting before retrying...")
                raise ValueError("Rate limited")
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(response.content)
            print(f"Downloaded {pdf_name} to {pdf_path}")
            break
        except Exception as e:
            wait = (2 ** attempt) + (random.randint(0, 1000) / 1000)
            print(f"Attempt {attempt+1} failed ({e}). Waiting {wait} seconds.")
            time.sleep(wait)
            attempt += 1

def download_pdfs(url, folder_path):
    base_url = 'https://arxiv.org'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find total number of entries
    total_entries_section = soup.find('small')
    total_entries_text = total_entries_section.text if total_entries_section else ""
    total_entries = int(total_entries_text.split()[3].replace(',', '')) if 'total of' in total_entries_text else 0
    print(f"Total entries: {total_entries}")

    entries_per_page = 2000
    number_of_pages = (total_entries // entries_per_page) + (1 if total_entries % entries_per_page > 0 else 0)
    
    for page in range(number_of_pages):
        skip = page * entries_per_page
        page_url = f"{base_url}/list/cs/24?skip={skip}&show=2000"
        print(f"Processing page: {page_url}")
        
        page_response = requests.get(page_url)
        page_soup = BeautifulSoup(page_response.content, 'html.parser')
        
        dts = page_soup.find_all('dt')
        for dt in dts:
            pdf_link = dt.find('a', title="Download PDF")
            dd = dt.find_next_sibling('dd')
            if pdf_link and dd:
                subject = dd.find('div', class_='list-subjects')
                if 'Artificial Intelligence (cs.AI)' in subject.text:
                    pdf_url = f"{base_url}{pdf_link['href']}"
                    pdf_name = pdf_url.split('/')[-1] + '.pdf'
                    pdf_path = os.path.join(folder_path, pdf_name)
                    
                    if os.path.exists(pdf_path):
                        print(f"{pdf_name} already exists. Skipping download.")
                    else:
                        download_pdf(pdf_url, pdf_path, pdf_name)
                else:
                    print("Skipping irrelevant subject...")
            else:
                print("Skipping entry due to missing PDF link or metadata.")
        time.sleep(10)  # Be respectful to the server, avoid getting rate limited

# URL to start scraping from
url = 'https://arxiv.org/list/cs/24?skip=0&show=2000'

# Use the current directory where the script is running as the folder path
folder_path = os.path.join(os.getcwd(), 'arxiv-pdfs')

# Execute the function
download_pdfs(url, folder_path)
