import json
import os
import re

# 🔹 Enable test mode (Set to True to auto-fill answers for testing)
test_mode = True

def test_input(prompt, default):
    """Returns a default value if test_mode is enabled, otherwise asks for input."""
    if test_mode:
        print(f"{prompt} {default}")  # Simulate user input for visibility
        return default
    return input(prompt).strip()

def validate_email():
    """Ensure user inputs a valid email format."""
    while True:
        email = test_input("Email:", "test@example.com")
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return email
        print("❌ Invalid email format. Please enter a valid email (e.g., user@example.com).")

def validate_phone():
    """Ensure phone number contains a country code and valid digits."""
    while True:
        phone = test_input("Phone Number (Include Country Code, e.g., +1 5551234567):", "+1 5551234567")
        if re.match(r"^\+\d{1,4}\s\d{8,15}$", phone):  # Regex to enforce country code and number
            return phone
        print("❌ Invalid phone number. Use format '+[Country Code] [Number]' (e.g., +1 5551234567).")

def optional_input(prompt, default="Not provided"):
    """Allows skipping fields by pressing Enter, or auto-fills in test mode."""
    return test_input(prompt, default)

def collect_user_info():
    """Collects personal and career details, then saves them in separate JSON files."""
    
    print("\n🚀 Personal Information (Stored in `user_data.json`)")

    user_data = {
        "first_name": test_input("First Name:", "John"),
        "last_name": test_input("Last Name:", "Doe"),
        "email": validate_email(),
        "phone": validate_phone(),
        "location": test_input("Location (City):", "New York"),
        "resume": optional_input("Resume/CV (Attach link, Dropbox, Google Drive, or press Enter to skip): ", "Not provided"),
        "cover_letter": optional_input("Cover Letter (Attach link, Dropbox, Google Drive, or press Enter to skip): ", "Not provided"),
        "linkedin": optional_input("LinkedIn Profile (or press Enter to skip): ", "Not provided"),
        "github": optional_input("GitHub Link (or press Enter to skip): ", "Not provided"),
        "work_auth": test_input("Are you legally authorized to work in the country where you are applying? (y/n):", "y").lower(),
        "visa_sponsorship": test_input("Will you now or in the future require visa sponsorship for employment? (y/n):", "n").lower()
    }

    print("\n🚀 Career Preferences (Stored in `user_profile.json`)")

    user_profile = {
        "preferred_job_titles": test_input("Preferred Job Titles (Comma-separated, e.g., 'Software Engineer, Data Analyst'):", "Software Engineer, Data Scientist"),
        "skills": test_input("Top Skills (Comma-separated, e.g., 'Python, Web Scraping, Machine Learning'):", "Python, Web Scraping, Automation"),
        "experience_years": optional_input("Years of Experience:", "3"),
        "desired_salary": optional_input("Desired Salary Range (e.g., '$80K - $100K' or 'Negotiable'):", "$80K - $100K"),
        "job_type": optional_input("Job Type (Remote, Hybrid, Onsite):", "Remote"),
        "industries": optional_input("Preferred Industries (e.g., 'Tech, Finance, Healthcare'):", "Tech, AI, Finance")
    }

    # 🔹 Save Personal Data (`user_data.json`)
    if os.path.exists("user_data.json"):
        if os.path.exists("user_data_backup.json"):
            os.remove("user_data_backup.json")  # Delete old backup first
        os.rename("user_data.json", "user_data_backup.json")

    with open("user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)

    # 🔹 Save Career Data (`user_profile.json`)
    if os.path.exists("user_profile.json"):
        if os.path.exists("user_profile_backup.json"):
            os.remove("user_profile_backup.json")  # Delete old backup first
        os.rename("user_profile.json", "user_profile_backup.json")

    with open("user_profile.json", "w") as file:
        json.dump(user_profile, file, indent=4)

    print("\n✅ User information saved! Ready for job scraping & automated applications.")

if __name__ == "__main__":
    collect_user_info()
