import numpy as np
import cohere
from annoy import AnnoyIndex
import warnings
import os


def load_paragraphs(directory) -> np.array:
    """ Loads all paragraphs from a directory
    Returns:
        np.array: Array of all paragraphs
    """
    texts = []
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                texts.extend(text.split('\n'))
    return np.array(texts)


def get_embeddings(texts, api_key):
    """ Gets the embeddings for all paragraphs
    
    Args:
        texts (list): List of all paragraphs
        api_key (str): API key for the Cohere API
        
    Returns:
        np.array: Array of embeddings for all paragraphs
    """
    co = cohere.Client(api_key)
    response = co.embed(texts=texts.tolist())
    return np.array(response.embeddings)


def build_search_index(embeddings):
    search_index = AnnoyIndex(embeddings.shape[1], 'angular')
    for i in range(len(embeddings)):
        search_index.add_item(i, embeddings[i])
    search_index.build(10)
    search_index.save('search_index.ann')
    return search_index


def search_for_context(query, search_index, texts, num_nearest=3):
    """ Searches for similar viewpoints to the query

    Args:
        query (str): The question to search for
        search_index (AnnoyIndex): The search index to use
        texts (list): List of all viewpoints, i.e. paragraphs/chunks of text

    Returns:
        list: List of nearest viewpoints to the query
    """
    co = cohere.Client(api_key)
    query_embed = co.embed(texts=[query]).embeddings
    similar_item_ids = search_index.get_nns_by_vector(
        query_embed[0], num_nearest, include_distances=True)
    search_results = [texts[i] for i in similar_item_ids[0]]
    return search_results


def generate_response(question, contexts, api_key):
    co = cohere.Client(api_key)
    
    cautions = """
        These are different views about the topic. Try to consider all of them with a critical eye.
        If some words at end or beginning of IDEAs are broken, please correct them; it must be typos.
    """

    prompt = f"""
    Excerpt from the articles provided 
    It is a complicated matter and not a simple question,
    therefore think carefully and weigh what you mean.

    Consider the following ideas by different thinkers:
    {'--- Another IDEA: '.join(contexts)}

    Question: {question}
    
    Please note:
    {cautions}

    Extract the answer of the question from the text provided.
    """

    prediction = co.generate(
        prompt=prompt.strip(),
        max_tokens=150,
        model="command-nightly",
        temperature=0.75,    
        # temperature determines the randomness/creativity of the response
        num_generations=1
    )

    return prediction.generations


if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    
    api_key = os.environ['COHERE_API_KEY']

    texts = load_paragraphs('processed_data/')
    
    embeddings = get_embeddings(texts, api_key)
    
    if os.path.exists('search_index.ann'):
        search_index = AnnoyIndex(embeddings.shape[1], 'angular')
        search_index.load('search_index.ann')
    else:
        search_index = build_search_index(embeddings)
    
    query = "What is the meaning of life?"
    viewpoints = search_for_context(query, search_index, texts, num_nearest=5)
    results = generate_response(query, viewpoints, api_key)
    print(results[0])