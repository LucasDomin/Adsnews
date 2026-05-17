import asyncio

from playwright.async_api import async_playwright


async def main():

    async with async_playwright() as p:

        browser = await p.chromium.launch(
            headless=False
        )

        page = await browser.new_page()

        url = (
            "https://www.facebook.com/ads/library/"
            "?active_status=active"
            "&ad_type=all"
            "&country=BR"
            "&q=emprestimo"
        )

        print("[*] Abrindo Meta Ads Library")

        await page.goto(
            url,
            wait_until="networkidle"
        )

        await asyncio.sleep(10)

        html = await page.content()

        with open(
            "page.html",
            "w",
            encoding="utf-8"
        ) as f:
            f.write(html)

        print("[+] page.html salvo")

        await browser.close()


asyncio.run(main())