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

    CHECKS_INFO = {
        'dns.A':          {'label': 'A Records',                'desc': 'IPv4 addresses for the domain.'},
        'dns.MX':         {'label': 'MX Records',               'desc': 'Mail exchange servers.'},
        'ssl.issuer':     {'label': 'SSL Issuer',               'desc': 'Certificate issuer information.'},
        'ssl.valid_from': {'label': 'Valid From',               'desc': 'Certificate start date.'},
        'ssl.valid_to':   {'label': 'Valid To',                 'desc': 'Certificate expiration date.'},
        'robots.lines':   {'label': 'Robots.txt Entries',       'desc': 'Rules in robots.txt.'},
        'ads_txt.entries_count': {'label': 'Ads.txt Count',     'desc': 'Number of valid ads.txt records.'},
        'ads_txt.entries':       {'label': 'Ads.txt Records',   'desc': 'Authorized sellers list.'},
        'sitemap.url_count':     {'label': 'Sitemap URLs',      'desc': 'Total URLs in sitemap.'},
        'tags.gam':       {'label': 'GAM Tag',                 'desc': 'Google Ad Manager tag detected.'},
        'tags.gtm':       {'label': 'GTM Tag',                 'desc': 'Google Tag Manager container detected.'},
        'tags.cmp':       {'label': 'CMP Scripts',             'desc': 'Consent management platforms detected.'},
        'malicious_js.meta_refresh': {'label': 'Meta Refresh',   'desc': 'Auto-redirect meta tag found.'},
        'malicious_js.hidden_iframes': {'label': 'Hidden Iframes', 'desc': 'Iframes with zero dimensions found.'},
    }

    structured = {}
    for category, res in raw_results.items():
        structured[category] = []
        for key, val in res.items():
            meta_key = f"{category}.{key}"
            info = CHECKS_INFO.get(meta_key, {'label': key.replace('_', ' ').title(), 'desc': ''})
            structured[category].append({
                'name': info['label'], 'description': info['desc'], 'value': val
            })
    return structured

@app.route('/', methods=['GET', 'POST'])
def index():
    report, domain = None, None
    if request.method == 'POST':
        domain = request.form['domain'].strip()
        if domain:
            report = asyncio.run(run_all_checks(domain))
            logger.info(f"Checks completed for {domain}")
    return render_template('index.html', report=report, domain=domain)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)