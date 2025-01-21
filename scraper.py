from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 🔹 Chromium Path (Ungoogled Chromium)
chromium_path = r"C:\Users\Ethan\AppData\Local\Chromium\Application\chrome.exe"

# 🔹 Set Up Chrome Options
options = Options()
options.binary_location = chromium_path  # Use Chromium
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")

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

            job_listings.append({
                "Source": site,
                "Title": title,
                "Company": company,
                "Location": location,
                "Apply Link": link
            })
        except Exception as e:
            print(f"❌ Error extracting job: {e}")

# 🔹 Save Jobs to CSV
df = pd.DataFrame(job_listings)
df.to_csv("job_listings.csv", index=False)
print("✅ Job listings saved!")

# 🔹 Close Browser
driver.quit()
