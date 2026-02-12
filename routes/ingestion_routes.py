from fastapi import APIRouter, Depends
from controllers.Ingestion_controller import submit_sitemap # The Controller
from pydantic import BaseModel
from core.loginAuth import verify_token, TokenData

class SitemapRequest(BaseModel):
    sitemap_url: str

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/sitemap")
async def handle_submit_sitemap(data: SitemapRequest, current_user: TokenData = Depends(verify_token)): # RENAME THIS FUNCTION
    """
    Route that receives the sitemap URL and delegates to the controller.
    Requires valid admin token in Authorization header.
    """
    # Now this correctly calls the imported 'submit_sitemap' from your controller
    return await submit_sitemap(data)