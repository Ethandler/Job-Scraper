from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json

# 🔹 Load User Preferences from `user_profile.json`
with open("user_profile.json", "r") as f:
    user_data = json.load(f)

preferred_titles = [title.lower().strip() for title in user_data["desired_job_titles"]]
preferred_skills = [skill.lower().strip() for skill in user_data["skills"]]

# 🔹 Chromium Path (Ungoogled Chromium)
chromium_path = r"C:\Users\Ethan\AppData\Local\Chromium\Application\chrome.exe"

# 🔹 Set Up Chrome Options (Now with SwiftShader Enabled)
options = Options()
options.binary_location = chromium_path  # Use Chromium
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")

# 🛠️ **Enable Software Rendering (SwiftShader)**
options.add_argument("--disable-gpu")  # Disable GPU acceleration
options.add_argument("--disable-software-rasterizer")  # Force software rendering

# 🔹 Initialize Selenium WebDriver (Uses system-installed chromedriver)
driver = webdriver.Chrome(options=options)

# 🔹 Job Sites to Scrape
job_sites = {
    "WeWorkRemotely": "https://weworkremotely.com/categories/remote-programming-jobs",
    "Remotive": "https://remotive.io/remote-jobs/software-dev"
}

# 🔹 Scrape Jobs
job_listings = []

for site, url in job_sites.items():
    driver.get(url)
    time.sleep(3)  # Let page load

    # 🔍 Extract Job Listings
    if site == "WeWorkRemotely":
        jobs = driver.find_elements(By.CSS_SELECTOR, "section.jobs article li a")

        for job in jobs:
            try:
                job_text = job.text.split("\n")  # Split text into lines
                title = job_text[0]  # First line is usually the job title
                company = job_text[1] if len(job_text) > 1 else "Unknown"  # Second line should be company name
                link = job.get_attribute("href")
                location = "Remote"

                # 🔍 **Filter Jobs Based on User Preferences**
                if any(title.lower() in job_title for job_title in preferred_titles) or any(
                        skill in title.lower() for skill in preferred_skills):
                    job_listings.append({
                        "Source": site,
                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Apply Link": link
                    })
            except Exception as e:
                print(f"❌ Error extracting job: {e}")

    elif site == "Remotive":
        jobs = driver.find_elements(By.CSS_SELECTOR, "div.job-tile a")

        for job in jobs:
            try:
                title = job.text.split("\n")[0]  # Extract title
                link = job.get_attribute("href")
                company = "Unknown"
                location = "Remote"

                # 🔍 **Filter Jobs Based on User Preferences**
                if any(title.lower() in job_title for job_title in preferred_titles) or any(
                        skill in title.lower() for skill in preferred_skills):
                    job_listings.append({
                        "Source": site,
                        "Title": title,
                        "Company": company,
                        "Location": location,
                        "Apply Link": link
                    })
            except Exception as e:
                print(f"❌ Error extracting job: {e}")

# 🔹 Save Filtered Jobs to CSV
df = pd.DataFrame(job_listings)
df.to_csv("job_listings.csv", index=False)
print(f"✅ {len(job_listings)} relevant jobs saved!")

# 🔹 Close Browser
driver.quit()
