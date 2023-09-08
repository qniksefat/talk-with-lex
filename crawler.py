import os
import requests
from bs4 import BeautifulSoup
import re

# fetch and process the text from a webpage
def process_webpage(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()

    # Remove unwanted lines
    text = '\n'.join(line.strip() for line in text.splitlines() if line.strip())

    # Apply regex to extract desired format
    text = re.sub(r'link \| \d{2}:\d{2}:\d{2}.\d{3} ', '', text)

    return text


def save_to_file(output_directory, file_number, text):
    with open(f'{output_directory}/{file_number}.txt', 'w', encoding='utf-8') as file:
        file.write(text)


# process text from a file
def process_text_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    lines = lines[2:]
    # Take every third line
    processed_text = ''.join(lines[2::3])
    return processed_text


def crawl_webpages():
    base_url = 'https://karpathy.ai/lexicap/'
    output_directory = 'raw_data/'

    # Create directory if not exists
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for file_number in range(1, 326):
        file_number_str = str(file_number).zfill(4)
        url = f'{base_url}{file_number_str}-large.html'

        text = process_webpage(url)

        save_to_file(output_directory, file_number_str, text)
        
        processed_text = process_text_file(f'{output_directory}/{file_number_str}.txt')
        save_to_file(output_directory, file_number_str, processed_text)


if __name__ == '__main__':
    crawl_webpages()
