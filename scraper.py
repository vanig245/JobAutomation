import time
import re
import json
import os
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"
SEEN_JOBS_FILE = "seen_jobs.json"

def load_seen_jobs():
    """Loads the list of previously processed jobs."""
    if os.path.exists(SEEN_JOBS_FILE):
        with open(SEEN_JOBS_FILE, "r") as f:
            return json.load(f)
    return []

def save_seen_job(job_id):
    """Saves a new job to the tracking file."""
    seen = load_seen_jobs()
    if job_id not in seen:
        seen.append(job_id)
        with open(SEEN_JOBS_FILE, "w") as f:
            json.dump(seen, f)

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
        print("Ensuring feed is sorted by 'Most recent'")
        try:
            sort_button = page.locator("button", has_text="Recommended").first
            if sort_button.is_visible():
                sort_button.click()
                time.sleep(1.5)

                recent_option = page.locator("text='Most recent'").first
                if recent_option.is_visible():
                    recent_option.click()
                    print("Changed sort order to 'Most recent'. Waiting for feed to refresh")
                    time.sleep(6)
                else:
                    sort_button.click()
            else:
                print("Feed is likely already sorted by 'Most recent'.")
        except Exception as e:
            print("Could not adjust sort order. Proceeding with current feed.")

        all_buttons = page.locator("button[data-test='LearnMoreButton']").all()
        buttons = all_buttons[:25]
        print(f"Found {len(all_buttons)} jobs in feed. Capping at {len(buttons)} for extraction...\n")

        scraped_jobs = []
        seen_jobs = load_seen_jobs()
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
                
                job_id = f"{company}::{title}"
                if job_id in seen_jobs:
                    print(f"[{index}/{len(buttons)}] Skipped: Already processed '{job_id}' in a previous run.")
                    page.keyboard.press("Escape")
                    time.sleep(1)
                    continue

                if re.search(r'posted:\s*([2-9]\s+weeks?|\d+\s+months?|\d+\s+years?)\s+ago', modal_text.lower()):
                    print(f"[{index}/{len(buttons)}]Skipped: Job is older than 1 week.")
                    save_seen_job(job_id)
                    page.keyboard.press("Escape")
                    time.sleep(1)
                    continue

                scraped_jobs.append({
                    "title": title,
                    "company": company,
                    "url": page.url,
                    "description": modal_text
                })

                print(f"[{index}/{len(buttons)}] Extracted: {title} at {company}")
                
                save_seen_job(job_id)

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