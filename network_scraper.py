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
 
        # Print every request made by the browser.
        page.on(
            "request",
            lambda request: print(
                "REQUEST:",
                request.method,
                request.url
            )
        )
 
        print("Opening RADAR...")
 
        await page.goto(
            RADAR_URL,
            wait_until="domcontentloaded"
        )
 
        # Give JavaScript time to make API requests.
        await page.wait_for_timeout(10000)
 
        print()
        print("Finished waiting.")
 
        await page.wait_for_timeout(3000)
 
        await browser.close()
 
 
if __name__ == "__main__":
    asyncio.run(main())
