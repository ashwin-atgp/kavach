import dns.resolver

def run(domain: str):
    result = {}
    # A records
    try:
        answers = dns.resolver.resolve(domain, 'A')
        result['A'] = [rdata.to_text() for rdata in answers]
    except Exception as e:
        result['A_error'] = str(e)
    # MX records
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        result['MX'] = [r.exchange.to_text() for r in answers]
    except Exception:
        pass
    return result