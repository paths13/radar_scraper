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
                print("=" * 60)
                print("COMPANY API FOUND")
                print("=" * 60)
 
                data = await response.json()
 
                print()
                print("Total companies:", data["total"])
 
                companies = data["result"]
 
                print("Companies in this response:", len(companies))
 
                print()
                print("COMPANIES")
                print("=" * 60)
 
                for number, company in enumerate(
                    companies,
                    start=1
                ):
 
                    name = company.get(
                        "organization",
                        {}
                    ).get(
                        "public_name"
                    )
 
                    email = company.get(
                        "public_email"
                    )
 
                    website = company.get(
                        "public_site"
                    )
 
                    print()
                    print(f"{number}. {name}")
                    print(f"   Email: {email}")
                    print(f"   Website: {website}")
 
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
 
        print("Waiting for company API...")
 
        await page.wait_for_timeout(10000)
 
        print()
        print("Finished.")
 
        await page.wait_for_timeout(3000)
 
        await browser.close()
 
 
if __name__ == "__main__":
    asyncio.run(main())
