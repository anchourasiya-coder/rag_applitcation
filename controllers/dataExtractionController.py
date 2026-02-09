from fastapi import HTTPException
from services.queryExtraction.queryHandler import perform_rag_extraction

async def process_query_request(request_data):
    try:
        # Controller calls the service to get the final answer
        result = await perform_rag_extraction(request_data.question)
        # result = await perform_rag_extraction(request_data)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))