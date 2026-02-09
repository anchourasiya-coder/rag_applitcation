import ollama

def generate_embeddings(chunks: list[str]):
    """
    Takes a list of cleaned text chunks and returns a list of embeddings.
    """
    if not chunks:
        return []

    # Using the 'embed' method for batch processing
    response = ollama.embed(
        model='mxbai-embed-large',
        # model='rjmalagon/gte-qwen2-1.5b-instruct-embed-f16',
        input=chunks
    )
    
    return response['embeddings']

