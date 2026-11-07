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

        print("Opening RADAR...")

        await page.goto(
            RADAR_URL,
            wait_until="domcontentloaded"
        )

        await page.wait_for_timeout(3000)

        title = await page.title()

        print(f"Page title: {title}")

        await page.screenshot(
            path="radar.png",
            full_page=True
        )

        print("Screenshot saved as radar.png")

        await page.wait_for_timeout(3000)

        await browser.close()


if __name__ == "__main__":
    asyncio.run(main())
