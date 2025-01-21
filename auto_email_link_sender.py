from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json
import random
import os
import numpy as np

# 🔹 Load User Preferences
with open("user_profile.json", "r") as f:
    user_data = json.load(f)

applied_companies_file = "applied_companies.json"
if os.path.exists(applied_companies_file):
    with open(applied_companies_file, "r") as f:
        applied_companies = set(json.load(f))
else:
    applied_companies = set()

# 🔹 Chromium Path (Ungoogled Chromium)
chromium_path = r"C:\Users\Ethan\AppData\Local\Chromium\Application\chrome.exe"

# 🔹 Set Up Chrome Options
options = Options()
options.binary_location = chromium_path  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")

# 🔹 Initialize WebDriver
driver = webdriver.Chrome(options=options)

# 🔹 Load Job Listings
df = pd.read_csv("job_listings.csv")

# 🔹 Test Mode (Set to False for Real Applications)
TEST_MODE = True  

# 🔹 Validate Required Columns
required_columns = {"Title", "Company", "Apply Link"}
missing_columns = required_columns - set(df.columns)

if missing_columns:
    print(f"🛑 ERROR: Missing columns in job_listings.csv: {missing_columns}")
    print("❌ Exiting. Please check the CSV file.")
    driver.quit()
    exit()

# 🔹 Check if "Posted" Column Exists Before Filtering
if "Posted" in df.columns:
    df["Posted"] = pd.to_datetime(df["Posted"], errors='coerce')
    df = df[df["Posted"] >= pd.Timestamp.now() - pd.Timedelta(days=21)]  # Only last 21 days
else:
    print("⚠️ Warning: 'Posted' column missing. Skipping date-based filtering.")

# 🔹 Remove Empty Apply Links
df = df.dropna(subset=["Apply Link"])
if df.empty:
    print("⚠️ Warning: No valid jobs with apply links found. Exiting.")
    driver.quit()
    exit()

# 🔹 Skip Already Applied Companies
df = df[~df["Company"].isin(applied_companies)]  

# 🔹 Limit Applications Per Run (15-30)
df = df.sample(n=random.randint(15, 30), random_state=42)

# 🔹 Helper Function to Click Elements Safely
def safe_click(driver, selector, by=By.CSS_SELECTOR, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, selector))
        )
        element.click()
        print(f"✅ Clicked {selector}")
        return True
    except Exception as e:
        print(f"⚠️ Could not click {selector}: {e}")
        return False

# 🔹 Navigate to Job Application Pages
def navigate_to_application(driver, apply_link):
    """Ensure we click the correct application button on each site."""
    
    driver.get(apply_link)
    time.sleep(3)

    if "remotive.io" in apply_link:
        print("🟤 Clicking 'Apply for this position' (Remotive - Brown Button)...")
        safe_click(driver, "a.remotive-btn-chocolate.tw-my-2.tw-relative")
        time.sleep(3)  

    elif "weworkremotely.com" in apply_link:
        print("🔴 Clicking 'Apply for this position' (WWR - Red Button)...")
        safe_click(driver, "a#job-cta-alt")
        time.sleep(3)  

# 🔹 Fill Out and Submit Application
def apply_to_job(driver, job):
    """Auto-fills application form and submits it"""

    # ❗ **Skip if Apply Link is Missing**
    if pd.isna(job["Apply Link"]):
        print(f"⚠️ Skipping {job['Title']} at {job['Company']} (No Apply Link)")
        return

    print(f"🚀 Applying for {job['Title']} at {job['Company']} ({job['Apply Link']})")

    navigate_to_application(driver, job['Apply Link'])

    if TEST_MODE:
        print(f"📝 [TEST MODE] Would type '{user_data['name']}' into Name field")
        print(f"📧 [TEST MODE] Would type '{user_data['email']}' into Email field")
        print(f"📜 [TEST MODE] Would upload resume '{user_data['resume_path']}'")
        print("🔄 [TEST MODE] Skipping actual submission.")
        return

    try:
        name_field = driver.find_element(By.NAME, "name")
        email_field = driver.find_element(By.NAME, "email")
        resume_upload = driver.find_element(By.NAME, "resume")

        name_field.send_keys(user_data["name"])
        email_field.send_keys(user_data["email"])
        resume_upload.send_keys(user_data["resume_path"])

        print("✅ Successfully entered details!")

        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        submit_button.click()
        print("🚀 Application submitted!")

        applied_companies.add(job["Company"])
        with open(applied_companies_file, "w") as f:
            json.dump(list(applied_companies), f, indent=4)

    except Exception as e:
        print(f"⚠️ Application failed for {job['Title']} at {job['Company']}: {e}")

# 🔹 Process Applications
for _, job in df.iterrows():
    apply_to_job(driver, job)

# 🔹 Close Browser
driver.quit()
print("\n✅ Auto-apply process completed.")
