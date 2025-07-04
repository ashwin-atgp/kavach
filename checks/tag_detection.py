from utils.http import fetch_text
from bs4 import BeautifulSoup
import re

def run(domain: str):
    status, text = fetch_text(f'https://{domain}')
    if status != 200:
        return {'error': f'status {status}'}
    soup = BeautifulSoup(text, 'lxml')
    tags = {}
    # GAM tags
    tags['gam'] = bool(re.search(r'googletag\.pubads', text))
    # GTM
    tags['gtm'] = bool(soup.find('script', src=re.compile(r'gtm\.js')))
    # Common CMPs
    cmp_scripts = ['OneTrust', 'Cookiebot', 'Quantcast']
    tags['cmp'] = [s for s in cmp_scripts if s in text]
    return tags