import json
import os
import re

# 🔹 Enable test mode (Set to True to auto-fill answers for testing)
test_mode = False

def test_input(prompt, default):
    """Returns a default value if test_mode is enabled, otherwise asks for input."""
    if test_mode:
        print(f"{prompt} [AUTO-FILLED] {default}")  # Debug print
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
    
    print("\n🚀 Starting User Input Collection...")

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
        "industries": optional_input("Preferred Industries (e.g., 'Tech, Finance, Healthcare'):", "Tech, AI, Finance"),
        "work_experience": []
    }

    # 🔹 Fix infinite loop issue
    if test_mode:
        # Add only ONE job experience in test mode
        user_profile["work_experience"].append({
            "title": "Software Engineer",
            "company": "Google",
            "years": "2",
            "description": "Developed scalable applications."
        })
    else:
        print("\n📜 Work Experience - Enter Past Jobs (Type 'done' to finish)")
        while True:
            job_title = test_input("Job Title:", "Software Engineer")
            if job_title.lower() == "done":
                break
            company = test_input("Company:", "Google")
            years = optional_input("Years at Company:", "2")
            description = optional_input("Brief Job Description:", "Developed scalable applications.")

            user_profile["work_experience"].append({
                "title": job_title,
                "company": company,
                "years": years,
                "description": description
            })

    # 🔹 Save Data
    print("\n💾 Saving user data...")

    with open("user_data.json", "w") as file:
        json.dump(user_data, file, indent=4)

    with open("user_profile.json", "w") as file:
        json.dump(user_profile, file, indent=4)

    print("\n✅ User information saved successfully!")

if __name__ == "__main__":
    print("\n🔹 Running user input script...")
    collect_user_info()
    print("\n🚀 User data collection complete. Now generating resume...")
    os.system("python resume_generator.py")
