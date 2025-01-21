from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# 🔹 Chromium Path
chromium_path = r"C:\Users\Ethan\AppData\Local\Chromium\Application\chrome.exe"

# 🔹 Set Up Chrome Options
options = Options()
options.binary_location = chromium_path
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")

# 🔹 Initialize Selenium WebDriver
driver = webdriver.Chrome(options=options)

# 🔹 Job Sites to Scrape
job_sites = {
    "WeWorkRemotely": "https://weworkremotely.com/categories/remote-programming-jobs",
    "Remotive": "https://remotive.io/remote-jobs/software-dev"
}

job_listings = []

for site, url in job_sites.items():
    driver.get(url)
    time.sleep(3)  # Let page load

    if site == "WeWorkRemotely":
        job_elements = driver.find_elements(By.CSS_SELECTOR, "section.jobs article ul li.feature a")

        for job in job_elements:
            try:
                link = job.get_attribute("href")
                job_listings.append({
                    "Source": site,
                    "Title": "N/A",
                    "Company": "N/A",
                    "Location": "Remote",
                    "Apply Link": link
                })
            except Exception as e:
                print(f"❌ Error extracting job on WeWorkRemotely: {e}")

    elif site == "Remotive":
        job_elements = driver.find_elements(By.CSS_SELECTOR, "li.tw-cursor-pointer a")

        for job in job_elements:
            try:
                link = job.get_attribute("href")
                job_listings.append({
                    "Source": site,
                    "Title": "N/A",
                    "Company": "N/A",
                    "Location": "Remote",
                    "Apply Link": link
                })
            except Exception as e:
                print(f"❌ Error extracting job on Remotive: {e}")

# 🔹 Save Jobs to CSV
df = pd.DataFrame(job_listings)
df.to_csv("job_listings.csv", index=False)
print(f"✅ {len(job_listings)} job links saved!")

# 🔹 Close Browser
driver.quit()
