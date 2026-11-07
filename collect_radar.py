import asyncio
import re
 
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
 
        # Give the website's JavaScript time to load the companies.
        await page.wait_for_timeout(3000)
 
        print("Finding company links...")
 
        # Find all links on the page.
        links = await page.locator("a[href]").evaluate_all(
            """
            elements => elements.map(a => ({
                text: a.innerText.trim(),
                href: a.href
            }))
            """
        )
 
        # Keep only links that point to company pages.
        companies = []
 
        for link in links:
 
            if "/companies/" in link["href"]:
 
                companies.append({
                    "name": link["text"],
                    "url": link["href"]
                })
 
        # Remove duplicate company links.
        unique_companies = []
 
        seen_urls = set()
 
        for company in companies:
 
            if company["url"] not in seen_urls:
 
                seen_urls.add(company["url"])
                unique_companies.append(company)
 
        # We only want the first 10 companies.
        unique_companies = unique_companies[:10]
 
        print(f"Found {len(unique_companies)} companies.")
        print()
 
        results = []
 
        # Visit each company page.
        for number, company in enumerate(unique_companies, start=1):
 
            print(f"{number}. Opening: {company['name']}")
 
            company_page = await browser.new_page()
 
            try:
 
                await company_page.goto(
                    company["url"],
                    wait_until="domcontentloaded"
                )
 
                await company_page.wait_for_timeout(1500)
 
                # First look for mailto links.
                email_links = await company_page.locator(
                    'a[href^="mailto:"]'
                ).evaluate_all(
                    """
                    elements => elements.map(a => a.href)
                    """
                )
 
                email = None
 
                if email_links:
 
                    email = email_links[0].replace(
                        "mailto:",
                        ""
                    ).split("?")[0]
 
                else:
 
                    # If there is no mailto link,
                    # search the visible page text.
                    text = await company_page.locator(
                        "body"
                    ).inner_text()
 
                    match = re.search(
                        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}",
                        text
                    )
 
                    if match:
                        email = match.group(0)
 
                results.append({
                    "name": company["name"],
                    "email": email,
                    "url": company["url"]
                })
 
                print(f"   Email: {email}")
 
            except Exception as error:
 
                print(f"   Error: {error}")
 
                results.append({
                    "name": company["name"],
                    "email": None,
                    "url": company["url"]
                })
 
            finally:
 
                await company_page.close()
 
        # Print final results.
        print()
        print("=" * 60)
        print("RESULTS")
        print("=" * 60)
 
        for result in results:
 
            print(
                f"{result['name']}  ->  "
                f"{result['email']}"
            )
 
        # Save results to a text file.
        with open(
            "radar_companies.txt",
            "w",
            encoding="utf-8"
        ) as file:
 
            for result in results:
 
                file.write(
                    f"Company: {result['name']}\n"
                )
 
                file.write(
                    f"Email: {result['email']}\n"
                )
 
                file.write(
                    f"URL: {result['url']}\n"
                )
 
                file.write("\n")
 
        print()
        print("Results saved to radar_companies.txt")
 
        await browser.close()
 
 
if __name__ == "__main__":
    asyncio.run(main())
