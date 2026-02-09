import xmltodict
import json

def convert_xml_to_json(xml_string: str):
    """
    Parses XML and returns a flat list of URL objects.
    """
    try:
        
        parsed_dict = xmltodict.parse(xml_string, xml_attribs=False)

        urls = parsed_dict.get('urlset', {}).get('url', [])

        # If xmltodict finds only ONE <url>, it might return a dict instead of a list.
        # This check ensures it is ALWAYS a list.
        if isinstance(urls, dict):
            return [urls]
            
        return urls

    except Exception as e:
        print(f"Error converting XML to JSON: {e}")
        return []