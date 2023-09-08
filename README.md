# Ask a question from Lex Fridman guests

This project lets you ask questions from Lex Fridman's podcast guests. While an official transcript isn't available, we've utilized web crawling techniques and utilized tools like Andrei Karpathy's Whisper to generate accurate transcripts.

## Data Preprocessing

We employed traditional techniques, leveraging libraries like NLTK and SpaCy, to split the gathered text into coherent paragraphs. This ensures that the context of each paragraph remains intact.

## Context and Clarity

Our approach emphasizes providing relevant context and clues to better frame the discussion. To achieve this, we use approximate nearest neighbors search methods with Annoy, a library developed by Spotify.

## Diverse Viewpoints

To offer a well-rounded perspective, we curate viewpoints from various individuals. We ensure that no single opinion on a topic is overrepresented, aiming for diversity in sentiments.

## Answering Questions with LLMs

We employ Large Language Models (LLMs) like Cohere to answer questions. By providing clear context and necessary cautions, we generate comprehensive responses.

## Usage

You can run processing.py to generate the necessary files. Then save your Cohere API key which you can get from [here](https://cohere.ai/) in the environment variable `COHERE_API_KEY`. The current `search_index.ann` has already been generated and is available in the repository.

To search for information, use the command line with a question like: `python search.py "What is the meaning of life?"`.
