import requests

def fetch_text(url, timeout=5):
    try:
        r = requests.get(url, timeout=timeout)
        return r.status_code, r.text
    except Exception as e:
        return None, str(e)