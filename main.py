import os
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def authenticate_wellfound():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            channel="chrome",
            headless=False,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = browser.new_context(viewport={"width": 1440, "height": 900})
        page = context.new_page()

        print("Navigating to Wellfound login")
        page.goto("https://wellfound.com/login")

        print("ACTION REQUIRED:")
        print("1. Complete your login in the opened Chrome window.")
        print("2. Ensure you are on your jobs feed or candidate dashboard.")
        print("3. Return here and press Enter to save your cookies.")

        input("Press Enter here AFTER you have successfully logged in: ")

        context.storage_state(path=AUTH_FILE)
        print(f"\nAuthenticated session successfully saved to {AUTH_FILE}")

        browser.close()

if __name__ == "__main__":
    authenticate_wellfound()