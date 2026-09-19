import time
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

AUTH_FILE = "job_state.json"

def scrape_jobs():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(storage_state=AUTH_FILE)
        page = context.new_page()

        page.goto("https://wellfound.com/jobs")
        
        print("Waiting for job feed to load")

        try:
            page.wait_for_selector("[data-test='JobCard']", timeout=20000)
        except Exception:
            print("Timeout: Could not find job cards. Ensure your selector is correct.")
            browser.close()
            return []
            
        jobs = []
        job_cards = page.locator("[data-test='JobCard']").all()
        print(f"Found {len(job_cards)} job cards. Extracting data...")
        
        for card in job_cards:
            try:
                card.click()
                time.sleep(1)

                title = card.locator("h2").first.inner_text()
                company = card.locator("h4").first.inner_text()
                apply_url = card.locator("a").first.get_attribute("href")
                description = page.locator(".styles_description__3v_3m").first.inner_text()
                
                jobs.append({
                    "title": title,
                    "company": company,
                    "url": f"https://wellfound.com{apply_url}" if apply_url.startswith("/") else apply_url,
                    "description": description
                })
                print(f"Extracted: {title} at {company}")
                
            except Exception as e:
                print(f"Skipped a card: missing required elements.")
                continue
                
        browser.close()
        return jobs

if __name__ == "__main__":
    extracted_data = scrape_jobs()
    print(f"\nTotal jobs successfully parsed: {len(extracted_data)}")