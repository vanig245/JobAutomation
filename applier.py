import time
import random
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def apply_to_jobs(approved_jobs, dry_run=True):
    if not approved_jobs:
        print("No approved jobs to process.")
        return []

    applied_jobs = []

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
        for index, job in enumerate(approved_jobs, start=1):
            print(f"\n[{index}/{len(approved_jobs)}] Opening application for: {job['title']} at {job['company']}")
            
            try:
                page.goto(job["url"], timeout=30000)
                time.sleep(random.uniform(2.5, 4.5)) 
                apply_button = page.locator("button:has-text('Apply'), button:has-text('Easy Apply'), button:has-text('Apply now')").first
                
                if not apply_button.is_visible():
                    print("'Apply' button not found. Skipping.")
                    continue

                apply_button.click()
                time.sleep(2.0)
                note_box = page.locator("textarea[name='userNote'], textarea[placeholder*='note'], textarea").first
                if note_box.count() > 0 and note_box.is_visible():
                    if note_box.is_enabled():
                        print("Typing AI-generated pitch")
                        note_box.click(force=True)
                        note_box.type(job["pitch"], delay=25)
                    else:
                        print("Pitch box is locked/disabled. Skipping pitch injection.")
                else:
                    print("No text box found for a pitch.")
                submit_button = page.locator("button:has-text('Send application'), button:has-text('Submit application')").first

                if dry_run:
                    print(f"[DRY RUN] Safely stopped. Would have clicked submit for {job['company']}.")
                    applied_jobs.append(job)
                else:
                    if submit_button.is_visible():
                        submit_button.click(force=True)
                        time.sleep(3)
                        print(f"Successfully applied to {job['company']}!")
                        applied_jobs.append(job)
                    else:
                        print("Submit button not found on the final screen.")

                time.sleep(random.uniform(3.0, 6.0))

            except Exception as e:
                print(f"Failed during application for {job['company']}: {e}")
                continue

        browser.close()
    return applied_jobs