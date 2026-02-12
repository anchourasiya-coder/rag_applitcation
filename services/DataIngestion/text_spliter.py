
from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_text_chunks(data, chunk_size=1000, chunk_overlap=100):
    """
    Takes in data (string or list of strings) and returns a list of chunks.
    """
    # 1. Handle case if data is a list (like your refined JSON objects)
    if isinstance(data, list):
        # Join list elements into one cohesive text block
        text_to_process = " ".join(data)
    else:
        text_to_process = data

    # 2. Initialize the splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        separators=["\n\n", "\n", " ", ""]
    )

    # 3. Perform the split
    chunks = text_splitter.split_text(text_to_process)
    
    return chunks