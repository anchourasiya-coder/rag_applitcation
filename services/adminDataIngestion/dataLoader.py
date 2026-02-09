import requests
from bs4 import BeautifulSoup

def scrape_sitemap_articles(data_list: list):
    """
    Scrapes the entire visible content of pages from a list of URLs.
    """
    scraped_results = []
    urls_to_scrape = []
    
    # Extract URLs from the data_list objects
    for item in data_list:
        for value in item.values():
            if isinstance(value, str) and value.startswith("http"):
                urls_to_scrape.append(value)
                break 

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    for url in urls_to_scrape:
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 1. Remove non-content elements (script, style, nav, footer)
            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()

            # 2. Target the <body> for the "whole page" data
            body_content = soup.find('body')
            
            if body_content:
                content = body_content.get_text(separator=' ', strip=True)
            else:
                content = soup.get_text(separator=' ', strip=True)

            scraped_results.append(content)

        except Exception as e:
            scraped_results.append(f"Error scraping {url}: {str(e)}")

    return scraped_results
