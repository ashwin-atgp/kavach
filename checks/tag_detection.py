# checks/tag_detection.py

import asyncio
from playwright.async_api import async_playwright

# List of CMP vendor keywords to search for
CMP_VENDORS = ["OneTrust", "Cookiebot", "Quantcast"]

async def run(domain: str):
    """
    Use a real browser UA via Playwright to fetch and render the page,
    then detect:
      • Google Ad Manager (GAM/GPT) tags
      • Google Tag Manager (GTM)
      • AdSense loader
      • Common Consent Management Platforms (CMPs)
    """

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        context = await browser.new_context(user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        ))
        page = await context.new_page()

        # Try HTTPS then HTTP
        for prefix in ("https://", "http://"):
            try:
                resp = await page.goto(f"{prefix}{domain}", timeout=15000)
                if resp and resp.status < 400:
                    break
            except Exception:
                continue

        content = await page.content()
        await browser.close()

    result = {}
    # Detect GAM/GPT (multiple core API calls)
    result["gam"] = bool(
        any(token in content for token in ["googletag.pubads", "googletag.defineSlot", "googletag.enableServices"])
    )

    # Detect GTM via script URL or dataLayer
    result["gtm"] = False
    for tag in ("googletagmanager.com/gtm.js?id=", "window.dataLayer"):
        if tag in content:
            result["gtm"] = True
            break

    # Detect AdSense via its loader
    result["adsense"] = "adsbygoogle.js" in content

    # Detect CMP vendors (case-insensitive search)
    lower = content.lower()
    result["cmp"] = [v for v in CMP_VENDORS if v.lower() in lower]

    return result


# If you need a synchronous wrapper:
def run_sync(domain: str):
    return asyncio.get_event_loop().run_until_complete(run(domain))
