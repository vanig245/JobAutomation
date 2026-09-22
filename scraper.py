import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def scrape_jobs():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ]
        )
        context = browser.new_context(
            storage_state=AUTH_FILE,
            viewport={"width": 1440, "height": 900}
        )
        page = context.new_page()
        print("Navigating to Wellfound jobs")

        page.goto("https://wellfound.com/jobs", wait_until="domcontentloaded")
        print("Waiting for feed hydration")
        page.wait_for_timeout(6000)
        job_card_locator = page.locator("article, [data-test='JobCard'], div[class*='styles_jobCard']").first
        
        try:
            job_card_locator.wait_for(timeout=15000)
            print("Job feed rendered successfully!")
        except Exception:
            print("Cards did not render in time. Checking page status")
            page.screenshot(path="debug_feed.png")
            browser.close()
            return []
        scraped_jobs = []
        cards = page.locator("article, div[class*='styles_jobCard']").all()
        print(f"Found {len(cards)} listings.")

        browser.close()
        return scraped_jobs

if __name__ == "__main__":
    scrape_jobs()