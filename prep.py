import os
import nltk
from nltk.tokenize import sent_tokenize

# Download the punkt tokenizer if not already downloaded
nltk.download('punkt')


def preprocess_paragraphs(file_number, input_text):
    """
    Preprocesses the input text by combining sentences into paragraphs and adding a file number identifier.

    Args:
        file_number (str)
        input_text (str): The input text to be preprocessed.
        
    Returns:
        paragraphs (list): A list of paragraphs, where each paragraph is a string.
    """
    
    # Tokenize text into sentences
    sentences = sent_tokenize(input_text)

    # Group sentences into paragraphs
    paragraphs = []
    current_paragraph = ""
    for sentence in sentences:
        current_paragraph += sentence + " "
        if sentence.endswith(('.', '!', '?')):
            paragraphs.append(current_paragraph.strip())
            current_paragraph = ""

    # Append the file number to the beginning of each paragraph
    paragraphs = [f'<<<{file_number}>>> ' + paragraph for paragraph in paragraphs]
    return paragraphs


def preprocess_chunks(file_number, input_text, chunk_size=2000):
    """
    Preprocesses the input text by chunking it into strings of a specified maximum length and adding a file number identifier.

    Args:
        chunk_size (int, optional): The maximum length of each chunk. Defaults to 2000.
        
    Returns:
        chunks (list): A list of text chunks, where each chunk is a string.
    """
    
    # Split input_text into chunks
    chunks = [input_text[i:i+chunk_size] for i in range(0, len(input_text), chunk_size)]

    # Append the file number to the beginning of each chunk
    chunks = [f'<<<{file_number}>>> ' + chunk for chunk in chunks]
    return chunks


def preprocess_directory(input_directory, output_directory, chunk_size=2000):
    """
    Preprocesses all text files in a directory and saves the preprocessed text in another directory.
    """
    for file_name in os.listdir(input_directory):
        if not file_name.endswith(".txt"):  continue
        
        file_path = os.path.join(input_directory, file_name)

        with open(file_path, 'r', encoding='utf-8') as file:
            input_text = file.read()
        
        file_number = file_name.split('.')[0]  # Extract file number from file name

        if chunk_size is None:
            processed_text = '\n'.join(preprocess_paragraphs(file_number, input_text))
        else:
            processed_text = '\n'.join(preprocess_chunks(file_number, input_text, chunk_size))

        output_file_path = os.path.join(output_directory, file_name)
        with open(output_file_path, 'w', encoding='utf-8') as file:
            file.write(processed_text)


if __name__ == '__main__':
    input_dir = 'raw_data/'
    output_dir = 'preprocessed_data/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Preprocess with chunking (2000 characters per chunk)
    preprocess_directory(input_dir, output_dir, chunk_size=2000)