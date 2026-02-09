import requests
from fastapi import APIRouter

router = APIRouter()


def get_sitemap_xml_raw(sitemap_url: str):

    if not sitemap_url:
        raise ValueError("No sitemap URL found")

    response = requests.get(sitemap_url, timeout=10)
    response.raise_for_status()

    return response.text  


def fetch_sitemap_xml(sitemap_url: str):
    xml = get_sitemap_xml_raw(sitemap_url)
    
    return xml
    