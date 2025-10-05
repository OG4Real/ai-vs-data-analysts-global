# src/clean_linkedin.py

import pandas as pd
import os

# Paths
RAW_PATH = "data/raw/linkedin_job_postings.csv"
PROCESSED_PATH = "data/processed/linkedin_job_postings_clean.csv"

# Load raw CSV
df = pd.read_csv(RAW_PATH)
print("CSV loaded successfully!")
print(f"Number of rows: {len(df)}")

# Define relevant job titles and roles
titles_of_interest = [
    "data analyst",
    "analyst",
    "statistician",
    "business analyst",
    "information analyst",
    "reporting analyst",
    "quantitative analyst",
    "data scientist"
]

# Filter relevant job titles (case-insensitive)
pattern = '|'.join(titles_of_interest)
df_filtered = df[df['title'].str.lower().str.contains(pattern, na=False)]

# Select only the columns we want
columns_to_keep = [
    'job_id', 
    'title', 
    'company_name', 
    'location', 
    'listed_time',  # post_date
    'description', 
    'min_salary',   # optional
    'max_salary',   # optional
    'med_salary',   # optional
    'posting_domain'  # for industry/sector mapping
]

# Keep only existing columns
columns_to_keep = [col for col in columns_to_keep if col in df_filtered.columns]
df_filtered = df_filtered[columns_to_keep]

# Rename columns for clarity
df_filtered.rename(columns={
    'listed_time': 'post_date',
    'company_name': 'company',
    'posting_domain': 'industry'
}, inplace=True)

# Convert post_date to datetime
df_filtered['post_date'] = pd.to_datetime(df_filtered['post_date'], errors='coerce')

# Save cleaned CSV
os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
df_filtered.to_csv(PROCESSED_PATH, index=False)

print("Cleaning complete!")
print(f"Cleaned dataset saved to {PROCESSED_PATH}")
print(f"Number of rows after filtering: {len(df_filtered)}")
