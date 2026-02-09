import uuid
from pinecone import Pinecone

def dump_embeds_to_pinecone(index_name,text_chunks, embeddings, namespace="default"):
    """
    Batches and pushes text chunks and their embeddings to Pinecone.
    """
    # 1. Prepare the records in the format Pinecone expects
    records = []
      # Initialize Pinecone client
    pc = Pinecone(api_key="pcsk_2haLb2_84fenM6XtXUmbJMLE5upS9RfsggSuix9DERf15BC4KgiodMYbNiTkuuEZq921BZ")

    # Connect to index
    index = pc.Index(index_name)
    for text, vector in zip(text_chunks, embeddings):
        # Create a unique ID for each chunk
        chunk_id = str(uuid.uuid4())
        
        records.append({
            "id": chunk_id,
            "values": vector,
            "metadata": {
                "text": text  # Storing the original text is essential for RAG
            }
        })

    # 2. Upsert in batches (Pinecone recommends ~100 per request)
    batch_size = 100
    for i in range(0, len(records), batch_size):
        batch = records[i : i + batch_size]
        index.upsert(vectors=batch, namespace=namespace)
        
    print(f"Successfully dumped {len(records)} embeddings to Pinecone.")


# import uuid
# from qdrant_client import QdrantClient
# from qdrant_client.models import PointStruct

# def dump_embeds_to_qdrant(collection_name, text_chunks, embeddings):
#     """
#     Batches and pushes text chunks and their embeddings to Qdrant Cloud.
#     """
#     # 1. Initialize Qdrant Cloud Client
#     # Replace with your actual credentials from your cluster dashboard
#     QDRANT_URL = "https://e3ff098b-4faf-4361-8b9b-14e7f172eda3.us-east4-0.gcp.cloud.qdrant.io:6333"
#     QDRANT_API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.uNsMb87G1k4ovuOnaTppWITzHTwgivs3gtGNt9umDXI"
    
#     client = QdrantClient(
#         url=QDRANT_URL,
#         api_key=QDRANT_API_KEY
#     )

#     # 2. Prepare the records (Points) in the format Qdrant expects
#     points = []
#     for text, vector in zip(text_chunks, embeddings):
#         # Qdrant supports UUID strings directly for IDs
#         chunk_id = str(uuid.uuid4())
        
#         points.append(PointStruct(
#             id=chunk_id,
#             vector=vector,
#             payload={
#                 "text": text  # Metadata is stored in the 'payload'
#             }
#         ))

#     # 3. Upsert into Qdrant
#     # Qdrant-client handles internal batching efficiently, but manual batching is also fine
#     try:
#         client.upsert(
#             collection_name=collection_name,
#             points=points,
#             wait=True # Wait for the changes to be committed
#         )
#         print(f"Successfully dumped {len(points)} embeddings to Qdrant Cloud.")
#     except Exception as e:
#         print(f"Error dumping to Qdrant: {str(e)}")