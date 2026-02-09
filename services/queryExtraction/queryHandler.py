# from fastapi import APIRouter, HTTPException
# from pydantic import BaseModel
# import ollama
# from pinecone import Pinecone
# from services.adminDataIngestion.embedsConverter import generate_embeddings

# router = APIRouter()

# class QueryRequest(BaseModel):
#     question: str
#     namespace: str = "default"

# # @router.post("/ask")
# # async def ask_question(request: QueryRequest):
# async def perform_rag_extraction(request):
#     try:
#         # 1. Initialization
#         API_KEY = "pcsk_2haLb2_84fenM6XtXUmbJMLE5upS9RfsggSuix9DERf15BC4KgiodMYbNiTkuuEZq921BZ"
#             # API_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.uNsMb87G1k4ovuOnaTppWITzHTwgivs3gtGNt9umDXI"
#         INDEX_NAME = "my-rag-index"
#         # INDEX_NAME = "my_rag_data"

#         pc = Pinecone(api_key=API_KEY)
    
#         index = pc.Index(INDEX_NAME)
        
#         # 2. Embedding: Convert query to vector
#         # mxbai-embed-large needs this specific prefix for queries    (1)
#         query_prefix = "Represent this sentence for searching relevant passages: "       
#         query_vector = generate_embeddings([query_prefix + request.question])[0]

#         # 3. Retrieval: Search Pinecone for top 3 matching chunks      (2) reranking with cohear
#         search_results = index.query(
#             vector=query_vector,
#             top_k=3,
#             namespace=request.namespace,
#             include_metadata=True  # Essential to get the 'text' back
#         )

#         # 4. Augmentation: Prepare context string 
#         context_chunks = [match['metadata']['text'] for match in search_results['matches']]
#         context_text = "\n\n".join(context_chunks)

#         # 5. Generation: Use the official Llama 3.1 Instruct Template
#         # Note the specific header tokens like <|begin_of_text|>, <|start_header_id|>, etc.    
#         prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
#         You are a helpful assistant. Use the following context to answer the user's question.
#         If the information is not in the context, say you don't know.
        
#         CONTEXT:
#         {context_text}
#         <|eot_id|><|start_header_id|>user<|end_header_id|>
#         {request.question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
#         """

#         response = ollama.generate(model='llama3.1:latest', prompt=prompt)

#         return {
#             "answer": response['response'],
#             "sources": context_chunks  # Return the chunks used for transparency
#         }
     
#         print('asnswer',response['response'])
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


import ollama
from qdrant_client import QdrantClient
from services.adminDataIngestion.embedsConverter import generate_embeddings

# Credentials from your Qdrant Dashboard
QDRANT_URL = "https://e3ff098b-4faf-4361-8b9b-14e7f172eda3.us-east4-0.gcp.cloud.qdrant.io:6333"
QDRANT_API_KEY ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.uNsMb87G1k4ovuOnaTppWITzHTwgivs3gtGNt9umDXI"
COLLECTION_NAME = "my_rag_data"

async def perform_rag_extraction(question: str):
    # 1. Initialize Qdrant Client
    client = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)

    # 2. Generate Embedding (Ensure your model output is 1536 dims)
    query_prefix = "Represent this sentence for searching relevant passages: "
    query_vector = generate_embeddings([query_prefix + question])[0]

    # # 3. Retrieval from Qdrant
    # search_results = client.search(
    #     collection_name=COLLECTION_NAME,
    #     query_vector=query_vector,
    #     limit=3,
    #     with_payload=True # Equivalent to Pinecone's include_metadata=True
    # )

    # # 4. Extract Text from Payload
    # # Qdrant stores metadata in 'payload' instead of 'metadata'
    # context_chunks = [hit.payload.get('text', '') for hit in search_results]
    # context_text = "\n\n".join(context_chunks)

    # 3. Retrieval from Qdrant (Updated Method)
    
    search_results = client.query_points(
    collection_name=COLLECTION_NAME,
    query=query_vector,   # Use 'query' instead of 'query_vector'
    limit=3,
    with_payload=True
    ).points  # .points is needed to get the list of hits from query_points

# 4. Extract Text from Payload (Updated for query_points)
    
    context_chunks = [hit.payload.get('text', '') for hit in search_results]
    context_text = "\n\n".join(context_chunks)

    # 5. Generation with Ollama (Llama 3.1 Template)
    #  print('reached there',context_text)
    prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
    You are a helpful assistant. Use the following context to answer the user's question.
    
    CONTEXT:
    {context_text}
    <|eot_id|><|start_header_id|>user<|end_header_id|>
    {question}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""
     
    response = ollama.generate(model='llama3.1:latest', prompt=prompt)
    
    print('reached there',response)
    return {
        "answer": response['response'],
        "sources": context_chunks
    }