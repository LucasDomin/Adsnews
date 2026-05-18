import asyncio
from playwright.async_api import async_playwright


URL = "https://www.facebook.com/ads/library/?q=emprestimo"


async def _scrape():
    try:
        async with async_playwright() as p:

            browser = await p.chromium.launch(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ]
            )

            context = await browser.new_context()
            page = await context.new_page()

            print("[SCRAPER] abrindo Meta Ads Library...")

            await page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            await page.wait_for_timeout(8000)

            html = await page.content()

            await browser.close()

            print("[SCRAPER] sucesso")
            return html

    except Exception as e:
        print(f"[SCRAPER ERROR] {e}")
        return ""


def run_scraper():
    return asyncio.run(_scrape())