import os
import requests
import pandas as pd
from dotenv import load_dotenv

# Load API credentials
load_dotenv()
APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")

SEARCH_TERMS = [
    "data analyst",
    "business analyst",
    "information analyst",
    "reporting analyst",
    "analytics specialist",
    "research analyst",
    "quantitative analyst"
]

def fetch_jobs(country="us", query="data analyst", results_per_page=50, page=1):
    url = f"https://api.adzuna.com/v1/api/jobs/{country}/search/{page}"
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "results_per_page": results_per_page,
        "what": query,
        "content-type": "application/json"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json().get("results", [])
    else:
        print("Error:", response.status_code, response.text)
        return []

# Collect results across terms & pages
records = []
for term in SEARCH_TERMS:
    for page in range(1, 11):  # 10 pages x 50 results = up to 500 per term
        jobs = fetch_jobs(country="us", query=term, results_per_page=50, page=page)
        if not jobs:
            break
        for job in jobs:
            records.append({
                "id": job.get("id"),
                "title": job.get("title"),
                "company": job.get("company", {}).get("display_name"),
                "location": job.get("location", {}).get("display_name"),
                "created": job.get("created"),
                "description": job.get("description"),
                "category": job.get("category", {}).get("label"),
                "search_term": term
            })
        print(f"Fetched {len(jobs)} jobs for '{term}' (page {page})")

# Save to CSV
df = pd.DataFrame(records).drop_duplicates(subset=["id"])
output_file = "data_analyst_related_jobs_us.csv"
df.to_csv(output_file, index=False, encoding="utf-8")

print(f"Saved {len(df)} job postings to {output_file}")
