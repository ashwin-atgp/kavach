# checks/tag_detection.py

from utils.http import fetch_text
from bs4 import BeautifulSoup
import re

def run(domain: str):
    """
    Detects presence of:
      • Google Ad Manager (GAM)
      • Google Tag Manager (GTM)
      • AdSense
      • Common Consent Management Platforms (CMPs)
    """

    # 1) Fetch page content over HTTPS or HTTP
    content = None
    for prefix in ('https://', 'http://'):
        status, text = fetch_text(f"{prefix}{domain}")
        if status and status < 400:
            content = text
            break
    if not content:
        return {'error': f'Failed to fetch page (status {status})'}

    soup = BeautifulSoup(content, 'lxml')
    result = {}

    # 2) GAM detection: look for multiple core GPT API calls
    gam_regex = r'googletag\.(pubads|defineSlot|enableServices)'
    result['gam'] = bool(re.search(gam_regex, content))

    # 3) GTM detection: check script src or inline dataLayer
    gtm = False
    for script in soup.find_all('script', src=True):
        if 'googletagmanager.com/gtm.js?id=' in script['src']:
            gtm = True
            break
    if not gtm and re.search(r'window\.dataLayer', content):
        gtm = True
    result['gtm'] = gtm

    # 4) AdSense detection via adsbygoogle loader
    result['adsense'] = any(
        'adsbygoogle.js' in script.get('src', '')
        for script in soup.find_all('script', src=True)
    )

    # 5) CMP detection: case-insensitive search for known vendor names
    cmp_vendors = ['OneTrust', 'Cookiebot', 'Quantcast']
    detected = []
    lower = content.lower()
    for vendor in cmp_vendors:
        if vendor.lower() in lower:
            detected.append(vendor)
    result['cmp'] = detected

    return result
