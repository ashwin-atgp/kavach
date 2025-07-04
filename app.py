from flask import Flask, render_template, request
import asyncio
from checks import (
    dns_checks, ssl_checks, robots_checks,
    ads_txt_checks, sitemap_checks, tag_detection,
    malicious_js_checks
)
from utils.logger import get_logger

logger = get_logger(__name__)
app = Flask(__name__)

async def run_all_checks(domain):
    results = {}
    results['dns'] = dns_checks.run(domain)
    results['ssl'] = ssl_checks.run(domain)
    results['robots'] = robots_checks.run(domain)
    results['ads_txt'] = ads_txt_checks.run(domain)
    results['sitemap'] = sitemap_checks.run(domain)
    results['tags'] = tag_detection.run(domain)
    results['malicious_js'] = await malicious_js_checks.run(domain)
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    report = None
    domain = None
    if request.method == 'POST':
        domain = request.form.get('domain').strip()
        if domain:
            logger.info(f"Running checks for {domain}")
            report = asyncio.run(run_all_checks(domain))
    return render_template('index.html', report=report, domain=domain)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)