import time
import re
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def scrape_jobs():
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

        print("Navigating to Wellfound jobs...")
        page.goto("https://wellfound.com/jobs", wait_until="domcontentloaded")

        print("Waiting for job listings to load...")
        try:
            page.wait_for_selector("button[data-test='LearnMoreButton']", timeout=15000)
        except Exception:
            print("No job listings found. Check your filters or session.")
            browser.close()
            return []

        all_buttons = page.locator("button[data-test='LearnMoreButton']").all()
        buttons = all_buttons[:10]
        print(f"Found {len(buttons)} jobs in feed. Extracting details...\n")

        scraped_jobs = []
        ui_noise = {"save", "apply", "applied", "share", "report", "hide", "close", "actively hiring", "recruiter recently active", "learn more"}

        for index, btn in enumerate(buttons, start=1):
            try:
                btn.scroll_into_view_if_needed()
                btn.click()
                time.sleep(2.5)

                modal = page.locator(".ReactModalPortal").last
                modal_text = modal.evaluate("el => el.innerText")
                raw_lines = [line.strip() for line in modal_text.splitlines() if line.strip()]
                content_lines = [line for line in raw_lines if line.lower() not in ui_noise]
                title = content_lines[0] if len(content_lines) > 0 else "Role"
                company = content_lines[1] if len(content_lines) > 1 else "Startup"

                scraped_jobs.append({
                    "title": title,
                    "company": company,
                    "url": page.url,
                    "description": modal_text
                })

                print(f"[{index}/{len(buttons)}] Extracted: {title} at {company}")

                page.keyboard.press("Escape")
                time.sleep(1)

            except Exception as e:
                print(f"[{index}/{len(buttons)}] Skipped: {e}")
                page.keyboard.press("Escape")
                time.sleep(1)
                continue

        browser.close()
        return scraped_jobs

if __name__ == "__main__":
    jobs = scrape_jobs()
    print(f"\nScraping complete! Successfully gathered {len(jobs)} fresh jobs.")