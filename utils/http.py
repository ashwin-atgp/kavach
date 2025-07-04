import requests

def fetch_text(url, timeout=5, headers=None):
    # default to a real‐browser User-Agent
    default_headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    if headers:
        default_headers.update(headers)

    try:
        resp = requests.get(url, timeout=timeout, headers=default_headers)
        return resp.status_code, resp.text
    except Exception as e:
        return None, str(e)
