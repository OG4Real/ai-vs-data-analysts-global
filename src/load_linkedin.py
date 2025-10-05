# src/load_linkedin.py
import pandas as pd

# Path to your CSV file
csv_path = "data/raw/linkedin_job_postings.csv"

# Load the CSV into a DataFrame
try:
    df = pd.read_csv(csv_path)
    print("CSV loaded successfully!")
    print(f"Number of rows: {len(df)}")
    print("Columns:", df.columns.tolist())
except PermissionError:
    print(f"Permission denied: cannot read {csv_path}")
except FileNotFoundError:
    print(f"File not found: {csv_path}")
