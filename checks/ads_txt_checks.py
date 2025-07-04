from utils.http import fetch_text

def run(domain: str):
    url = f'https://{domain}/ads.txt'
    status, text = fetch_text(url)
    if status != 200:
        return {'error': f'status {status}'}
    entries = [l.strip() for l in text.splitlines() if l.strip() and not l.startswith('#')]
    return {'entries_count': len(entries), 'entries': entries}