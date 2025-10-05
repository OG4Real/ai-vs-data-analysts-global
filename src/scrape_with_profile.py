# scrape_google_jobs.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time, pandas as pd
from bs4 import BeautifulSoup

# --- CONFIG ---
chromedriver_path = r"C:\Users\Admin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
search_titles = ["data analyst jobs", "business analyst jobs"]
max_results = 5  # Number of SERP results per search

# --- DRIVER SETUP ---
service = Service(executable_path=chromedriver_path)
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(service=service, options=options)

# --- MANUAL VERIFICATION ---
driver.get("https://www.google.com/")
print(">>> Please solve any CAPTCHA/login in Chrome. Waiting 15 seconds...")
time.sleep(15)

all_jobs = []

# --- SEARCH GOOGLE SERPS ---
for title in search_titles:
    query = title.replace(" ", "+")
    url = f"https://www.google.com/search?q={query}"
    driver.get(url)
    time.sleep(5)

    links = driver.find_elements(By.CSS_SELECTOR, "div.yuRUbf > a")  # SERP result links
    links = links[:max_results]

    for link in links:
        href = link.get_attribute("href")
        print(f"Visiting: {href}")
        try:
            driver.get(href)
            time.sleep(5)
            
            soup = BeautifulSoup(driver.page_source, "html.parser")

            # --- TRY EXTRACTING JOBS ---
            titles = [t.get_text(strip=True) for t in soup.find_all(["h1", "h2", "h3"]) if "job" in t.get_text().lower()]
            descs = [p.get_text(strip=True) for p in soup.find_all("p")[:5]]

            if titles:
                all_jobs.append({
                    "searched_title": title,
                    "page_url": href,
                    "job_title": titles[0],
                    "description": " ".join(descs[:2]) if descs else None
                })

        except Exception as e:
            print(f"Failed to scrape {href}: {e}")
            continue

# --- SAVE ---
df = pd.DataFrame(all_jobs)
df.to_csv("data/processed/google_jobs.csv", index=False)
print(f"Saved {len(df)} job postings to data/processed/google_jobs.csv")

driver.quit()
