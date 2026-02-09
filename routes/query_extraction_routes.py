from fastapi import APIRouter
from controllers.data_extraction_controller import process_query_request
from pydantic import BaseModel

router = APIRouter(prefix="/query", tags=["Retrieval"])

class QueryRequest(BaseModel):
    question: str
    namespace: str = "default"

@router.post("/ask")
async def ask_question(request: QueryRequest):
    # Route only passes data to the controller
    return await process_query_request(request)