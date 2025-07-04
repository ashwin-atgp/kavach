import asyncio
from playwright.async_api import async_playwright

async def run(domain: str):
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(f'https://{domain}', timeout=15000)
        meta = await page.query_selector('meta[http-equiv="refresh"]')
        frames = await page.query_selector_all('iframe')
        hidden = []
        for f in frames:
            box = await f.bounding_box()
            if box and (box['width'] == 0 or box['height'] == 0):
                hidden.append(await f.get_attribute('src'))
        await browser.close()
        return {'meta_refresh': bool(meta), 'hidden_iframes': hidden}