# scrape_linkedin_selenium_full_v2.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# --- CONFIGURATION ---
chromedriver_path = r"C:\Users\Admin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
linkedin_email = "your email"
linkedin_password = "your password"

search_titles = [
    "data analyst", "analyst", "business analyst", 
    "financial analyst", "statistician", "information analyst"
]

max_pages = 5  # Number of pages to scrape per title
sleep_time = 5  # Seconds to wait after loading page

# --- SETUP CHROME DRIVER ---
service = Service(executable_path=chromedriver_path)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# --- LINKEDIN LOGIN ---
driver.get("https://www.linkedin.com/login")
time.sleep(2)
driver.find_element(By.ID, "username").send_keys(linkedin_email)
driver.find_element(By.ID, "password").send_keys(linkedin_password)
driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
time.sleep(5)

# --- SCRAPE JOBS ---
all_jobs = []
seen_jobs = set()  # To skip duplicates

for title in search_titles:
    print(f"Scraping jobs for: {title}")
    
    for page in range(max_pages):
        start = page * 25  # 25 jobs per page
        try:
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={title.replace(' ', '%20')}&location=United%20States&start={start}"
            driver.get(search_url)
            time.sleep(sleep_time)

            job_cards = driver.find_elements(By.CSS_SELECTOR, "div.job-card-container")
            
            if not job_cards:
                print(f"No jobs found on page {page+1} for {title}")
                break

            for job in job_cards:
                try:
                    job_title = job.find_element(By.CSS_SELECTOR, "a.job-card-list__title--link").text
                    company = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__subtitle span").text
                    location = job.find_element(By.CSS_SELECTOR, "ul.job-card-container__metadata-wrapper li span").text

                    # Optional: salary if present
                    try:
                        salary = job.find_element(By.CSS_SELECTOR, "div.artdeco-entity-lockup__metadata span").text
                    except:
                        salary = None

                    # Optional: posted date if present
                    try:
                        posted_date = job.find_element(By.CSS_SELECTOR, "time").get_attribute("datetime")
                    except:
                        posted_date = None

                    # Optional: job type (full-time, part-time, etc.)
                    try:
                        job_type = job.find_element(By.CSS_SELECTOR, "div.job-card-container__metadata-wrapper span").text
                    except:
                        job_type = None

                    # Skip duplicates
                    job_key = (job_title.lower(), company.lower(), location.lower())
                    if job_key in seen_jobs:
                        continue
                    seen_jobs.add(job_key)

                    all_jobs.append({
                        "title": job_title,
                        "company": company,
                        "location": location,
                        "salary": salary,
                        "posted_date": posted_date,
                        "job_type": job_type,
                        "searched_title": title
                    })

                except:
                    continue

        except Exception as e:
            print(f"Failed to fetch page {page+1} for {title}: {e}")
            continue

# --- SAVE RESULTS ---
df = pd.DataFrame(all_jobs)
df.to_csv("data/processed/linkedin_us_jobs_full_v2.csv", index=False)
print(f"Saved {len(df)} job postings to data/processed/linkedin_us_jobs_full_v2.csv")

# --- CLEANUP ---
driver.quit()
