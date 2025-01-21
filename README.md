# 🚀 JobScraper - Automated Job Search & Application Bot

### **🔥 Overview**
JobScraper is an **automated job scraping tool** that:
- 🏆 **Finds remote & tech jobs** from multiple websites
- 🎯 **Filters jobs based on your skills, experience & preferences**
- 🤖 **Auto-fills applications** for relevant job postings
- 📝 **Future Features**: AI-powered matching & resume generation

---

### **📌 Features**
✅ Scrapes **job listings** from sites like WeWorkRemotely & Remotive  
✅ Uses **custom filters** (keywords, salary, job type)  
✅ Saves results to `joblistings.csv`  
✅ Auto-fills job applications using **Selenium**  
✅ Works with **VPN for anonymity**  

---

### **📥 Installation & Setup**
#### **1️⃣ Install Dependencies**
```sh
pip install -r requirements.txt
If chromedriver isn’t found, make sure it’s installed and in PATH.
2️⃣ Set Up Your Info
sh
Copy
Edit
python user_input.py
Fill out your details (name, email, skills, GitHub, LinkedIn, etc.)
These will be used to match jobs & auto-apply!
3️⃣ Run the Scraper
sh
Copy
Edit
python scraper.py
This will collect job listings into joblistings.csv
4️⃣ Auto-Apply to Jobs
sh
Copy
Edit
python auto_apply.py
This will submit applications to relevant jobs 🎯