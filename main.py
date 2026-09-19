import os
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def authenticate_wellfound():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=False, 
            args=["--disable-blink-features=AutomationControlled"]
        )
        
        if os.path.exists(AUTH_FILE):
            context = browser.new_context(storage_state=AUTH_FILE)
            print("Session loaded.")
        else:
            context = browser.new_context()
            print("Manual login required.")
            
        page = context.new_page()
        page.goto("https://wellfound.com/jobs")
        
        if not os.path.exists(AUTH_FILE):
            print("Please log in to Wellfound in the opened browser")
            page.wait_for_url("https://wellfound.com/jobs*", timeout=120000)
            context.storage_state(path=AUTH_FILE)
            print(f"Session cookies saved to {AUTH_FILE}")
            
        browser.close()

if __name__ == "__main__":
    authenticate_wellfound()