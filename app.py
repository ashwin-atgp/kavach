from flask import Flask, render_template, request, url_for
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
    raw_results = {}
    raw_results['dns'] = dns_checks.run(domain)
    raw_results['ssl'] = ssl_checks.run(domain)
    raw_results['robots'] = robots_checks.run(domain)
    raw_results['ads_txt'] = ads_txt_checks.run(domain)
    raw_results['sitemap'] = sitemap_checks.run(domain)
    raw_results['tags'] = tag_detection.run(domain)
    raw_results['malicious_js'] = await malicious_js_checks.run(domain)

    # Structure results with human-readable labels and descriptions
    CHECKS_INFO = {
        'dns.A':      {'label': 'A Records',             'desc': 'Lists IPv4 addresses for the domain.'},
        'dns.MX':     {'label': 'MX Records',            'desc': 'Lists mail exchange servers for the domain.'},
        'ssl.issuer': {'label': 'SSL Issuer',            'desc': 'Certificate issuer details.'},
        'ssl.valid_from': {'label': 'Valid From',        'desc': 'Certificate start date.'},
        'ssl.valid_to':   {'label': 'Valid To',          'desc': 'Certificate expiration date.'},
        'robots.lines':{'label': 'Robots.txt Lines',      'desc': 'All directives in robots.txt file.'},
        'ads_txt.entries_count': {'label': 'ads.txt Entries Count', 'desc': 'Number of valid entries in ads.txt.'},
        'ads_txt.entries':       {'label': 'ads.txt Entries',       'desc': 'List of authorized sellers from ads.txt.'},
        'sitemap.url_count':     {'label': 'Sitemap URL Count',    'desc': 'Number of URLs listed in sitemap.xml.'},
        'tags.gam':             {'label': 'GAM Tag',              'desc': 'Detects presence of Google Ad Manager tags.'},
        'tags.gtm':             {'label': 'GTM Tag',              'desc': 'Detects presence of Google Tag Manager containers.'},
        'tags.cmp':             {'label': 'CMP Scripts',          'desc': 'Lists detected consent management platforms.'},
        'malicious_js.meta_refresh': {'label': 'Meta Refresh',   'desc': 'Detects meta-refresh tags used for auto redirects.'},
        'malicious_js.hidden_iframes': {'label': 'Hidden Iframes','desc': 'Lists iframes with zero width or height.'},
    }

    structured = {}
    for category, res in raw_results.items():
        structured[category] = []
        for key, val in res.items():
            meta_key = f"{category}.{key}"
            info = CHECKS_INFO.get(meta_key, {'label': key.replace('_', ' ').title(), 'desc': ''})
            structured[category].append({
                'name': info['label'],
                'description': info['desc'],
                'value': val
            })
    return structured

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