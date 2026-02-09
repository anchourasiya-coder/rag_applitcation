from fastapi import APIRouter
from controllers.Ingestion_controller import submit_sitemap # The Controller
from pydantic import BaseModel

class SitemapRequest(BaseModel):
    sitemap_url: str

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/sitemap")
async def handle_submit_sitemap(data: SitemapRequest): # RENAME THIS FUNCTION
    """
    Route that receives the sitemap URL and delegates to the controller.
    """
    # Now this correctly calls the imported 'submit_sitemap' from your controller
    return await submit_sitemap(data)