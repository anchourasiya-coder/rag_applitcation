from bs4 import BeautifulSoup
import re

def clean_html_content(html_string: str):
    if not html_string:
        return ""
        
    # Standardize the input: BeautifulSoup works best with standard HTML
    soup = BeautifulSoup(html_string, 'html.parser')
    
    # 1. Remove non-content tags
    for element in soup(["script", "style", "header", "footer", "nav"]):
        element.decompose()

    # 2. Get text with a space separator
    clean_text = soup.get_text(separator=" ")

    # 3. Robust Whitespace Cleaning
    # This regex replaces multiple spaces/newlines/tabs with a single space
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()

    return clean_text