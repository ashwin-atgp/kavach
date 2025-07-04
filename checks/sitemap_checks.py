from utils.http import fetch_text
import xml.etree.ElementTree as ET

def run(domain: str):
    url = f'https://{domain}/sitemap.xml'
    status, text = fetch_text(url)
    if status != 200:
        return {'error': f'status {status}'}
    try:
        tree = ET.fromstring(text)
        urls = [elem.text for elem in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
        return {'url_count': len(urls)}
    except ET.ParseError as e:
        return {'error': str(e)}