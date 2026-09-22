import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def inspect_feed():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(
            storage_state=AUTH_FILE,
            viewport={"width": 1440, "height": 900}
        )
        page = context.new_page()

        print("Opening Wellfound jobs with saved session...")
        page.goto("https://wellfound.com/jobs", wait_until="domcontentloaded")

        time.sleep(5)

        print("\nOpening Playwright Inspector")
        print("1. Click the 'Pick locator' button in the Inspector window.")
        print("2. Hover over a job card and note the selector.")
        page.pause()

        browser.close()

if __name__ == "__main__":
    inspect_feed()