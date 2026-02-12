from fastapi import APIRouter
from pydantic import BaseModel

from services.DataIngestion.fetch_xml_service import fetch_sitemap_xml
from services.DataIngestion.convert_xml_to_url import convert_xml_to_json
from services.DataIngestion.data_scrape_service import scrape_sitemap_data
from services.DataIngestion.data_extraction import clean_html_content
from services.DataIngestion.text_spliter import create_text_chunks
from services.DataIngestion.chunk_to_embeds_converter import generate_embeddings
from services.DataIngestion.embeds_insertion import data_insertion

router = APIRouter()

LATEST_SITEMAP_URL = ""

class SitemapRequest(BaseModel):
    sitemap_url: str


# @router.post("/sitemap")
async def submit_sitemap(data: SitemapRequest):
    global LATEST_SITEMAP_URL


    LATEST_SITEMAP_URL = data.sitemap_url
 
    xml=fetch_sitemap_xml(LATEST_SITEMAP_URL)
    json_data = convert_xml_to_json(xml)
    scraped_data = scrape_sitemap_data(json_data)
   
    convertedContentList = [clean_html_content(html) for html in scraped_data]
    chunk_data=create_text_chunks(convertedContentList)

    embeds=generate_embeddings(chunk_data)

    data_insertion("my_rag_data",chunk_data,embeds)
    return {
        "message": "Sitemap URL received",
        "xml_preview": xml[:500],
        "data": json_data,
        "scraped_data":scraped_data,
        "convertedContent" : convertedContentList,
        "chunk_data":chunk_data,
        "embeds":embeds,
    }


