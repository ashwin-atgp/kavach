from utils.http import fetch_text

def run(domain: str):
    url = f'https://{domain}/robots.txt'
    status, text = fetch_text(url)
    if status != 200:
        return {'error': f'status {status}'}
    lines = [l for l in text.splitlines()]
    return {'lines': lines}