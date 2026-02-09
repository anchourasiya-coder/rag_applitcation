from fastapi import APIRouter
from pydantic import BaseModel

from services.adminDataIngestion.adminDataConverter import fetch_sitemap_xml
from services.adminDataIngestion.dataParser import convert_xml_to_json
from services.adminDataIngestion.dataLoader import scrape_sitemap_articles
from services.adminDataIngestion.dataExtraction import clean_html_content
from services.adminDataIngestion.textSpliter import create_text_chunks
from services.adminDataIngestion.embedsConverter import generate_embeddings
from services.adminDataIngestion.embedsDump import dump_embeds_to_pinecone

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
    scraped_data = scrape_sitemap_articles(json_data)
   
    convertedContentList = [clean_html_content(html) for html in scraped_data]
    chunk_data=create_text_chunks(convertedContentList)

    embeds=generate_embeddings(chunk_data)

    dump_embeds_to_pinecone("my_rag_data",chunk_data,embeds)
    return {
        "message": "Sitemap URL received",
        "xml_preview": xml[:500],
        "data": json_data,
        "scraped_data":scraped_data,
        "convertedContent" : convertedContentList,
        "chunk_data":chunk_data,
        "embeds":embeds,
    }


