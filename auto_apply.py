import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 🔹 Load User Profile
with open("user_profile.json", "r") as f:
    user_data = json.load(f)

name = user_data["name"]
email = user_data["email"]
github = user_data.get("github", "")
linkedin = user_data.get("linkedin", "")

# 🔹 Load Job Listings
df = pd.read_csv("job_listings.csv")
apply_links = df["Apply Link"].tolist()

# 🔹 Chromium Path (Ungoogled Chromium)
chromium_path = r"C:\Users\Ethan\AppData\Local\Chromium\Application\chrome.exe"

# 🔹 Set Up Chrome Options (Enable Software Rendering)
options = Options()
options.binary_location = chromium_path  # Use Chromium
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-gpu")
options.add_argument("--disable-software-rasterizer")  # Force software rendering

# 🔹 Initialize Selenium WebDriver
driver = webdriver.Chrome(options=options)

# 🔹 Auto-Fill Applications
for link in apply_links:
    try:
        print(f"🔹 Opening job application: {link}")
        driver.get(link)
        time.sleep(3)  # Let the page load

        # Try locating form fields
        try:
            name_field = driver.find_element(By.NAME, "name")
            email_field = driver.find_element(By.NAME, "email")
        except:
            print(f"⚠️ Skipping {link} - No standard form found")
            continue

        # Fill in the form fields
        name_field.send_keys(name)
        email_field.send_keys(email)

        if linkedin:
            try:
                linkedin_field = driver.find_element(By.NAME, "linkedin")
                linkedin_field.send_keys(linkedin)
            except:
                print("🔹 LinkedIn field not found, skipping it.")

        if github:
            try:
                github_field = driver.find_element(By.NAME, "github")
                github_field.send_keys(github)
            except:
                print("🔹 GitHub field not found, skipping it.")

        # Submit the application
        try:
            submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            submit_button.click()
            print(f"✅ Successfully applied to: {link}")
        except:
            print(f"⚠️ No submit button found on {link}, skipping.")

        time.sleep(2)  # Wait a bit before the next application

    except Exception as e:
        print(f"❌ Error applying to {link}: {e}")

# 🔹 Close Browser
driver.quit()
print("🚀 Auto-Apply Finished!")
