import asyncio
 
from playwright.async_api import async_playwright
 
 
RADAR_URL = (
    "https://radar.leader-id.ru/companies/it/ai"
    "?skip=0&limit=10&technologies=9"
)
 
 
async def main():
 
    async with async_playwright() as p:
 
        browser = await p.chromium.launch(
            headless=False
        )
 
        page = await browser.new_page()
 
        async def handle_response(response):
 
            if "/api/v2/site/company/search/global/public" in response.url:
 
                print()
                print("=" * 80)
                print("FOUND COMPANY API RESPONSE")
                print("=" * 80)
 
                print()
                print("STATUS:")
                print(response.status)
 
                print()
                print("URL:")
                print(response.url)
 
                print()
                print("JSON:")
                print(await response.text())
 
                print()
                print("=" * 80)
 
        page.on(
            "response",
            handle_response
        )
 
        print("Opening RADAR...")
 
        await page.goto(
            RADAR_URL,
            wait_until="domcontentloaded"
        )
 
        print("Page opened.")
 
        print("Waiting for API response...")
 
        await page.wait_for_timeout(10000)
 
        print()
        print("Finished waiting.")
 
        await page.wait_for_timeout(3000)
 
        await browser.close()
 
 
if __name__ == "__main__":
    asyncio.run(main())
