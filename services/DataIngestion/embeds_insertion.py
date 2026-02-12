# import uuid
# from pinecone import Pinecone

# def data_insertion(index_name,text_chunks, embeddings, namespace="default"):
#     """
#     Batches and pushes text chunks and their embeddings to Pinecone.
#     """
#     # 1. Prepare the records in the format Pinecone expects
#     records = []
#       # Initialize Pinecone client
#     pc = Pinecone(api_key="pcsk_2haLb2_84fenM6XtXUmbJMLE5upS9RfsggSuix9DERf15BC4KgiodMYbNiTkuuEZq921BZ")

#     # Connect to index
#     index = pc.Index(index_name)
#     for text, vector in zip(text_chunks, embeddings):
#         # Create a unique ID for each chunk
#         chunk_id = str(uuid.uuid4())
        
#         records.append({
#             "id": chunk_id,
#             "values": vector,
#             "metadata": {
#                 "text": text  # Storing the original text is essential for RAG
#             }
#         })

#     # 2. Upsert in batches (Pinecone recommends ~100 per request)
#     batch_size = 100
#     for i in range(0, len(records), batch_size):
#         batch = records[i : i + batch_size]
#         index.upsert(vectors=batch, namespace=namespace)
        
#     print(f"Successfully dumped {len(records)} embeddings to Pinecone.")

import os 
import uuid
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

load_dotenv()  # Load environment variables from .env file

def data_insertion(collection_name, text_chunks, embeddings):
    """
    Batches and pushes text chunks and their embeddings to Qdrant Cloud.
    """
    # 1. Initialize Qdrant Cloud Client
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    client = QdrantClient(
        url=QDRANT_URL,
        api_key=QDRANT_API_KEY
    )

    # 2. Prepare the records (Points) in the format Qdrant expects
    points = []
    for text, vector in zip(text_chunks, embeddings):
        # Qdrant supports UUID strings directly for IDs
        chunk_id = str(uuid.uuid4())
        
        points.append(PointStruct(
            id=chunk_id,
            vector=vector,
            payload={
                "text": text  # Metadata is stored in the 'payload'
            }
        ))

    # 3. Upsert into Qdrant
    # Qdrant-client handles internal batching efficiently, but manual batching is also fine
    try:
        client.upsert(
            collection_name=collection_name,
            points=points,
            wait=True # Wait for the changes to be committed
        )
        print(f"Successfully dumped {len(points)} embeddings to Qdrant Cloud.")
    except Exception as e:
        print(f"Error dumping to Qdrant: {str(e)}")