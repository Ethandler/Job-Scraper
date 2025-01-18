import requests # type: ignore

def fetch_jobs(location=None, remote_only=True):
    # API Endpoint
    url = "https://arbeitnow.com/api/job-board-api"

    try:
        # Fetch data from the API
        response = requests.get(url)
        response.raise_for_status()  # Ensure the request was successful

        # Parse the JSON response
        data = response.json()
        jobs = data.get("data", [])

        # Filter jobs
        filtered_jobs = []
        for job in jobs:
            job_title = job.get("title", "Unknown")
            company_name = job.get("company_name", "Unknown")
            job_location = job.get("location", "Unknown")
            job_remote = job.get("remote", False)
            job_url = job.get("url", "No URL Provided")

            # Apply filters
            if remote_only and not job_remote:
                continue
            if location and location.lower() not in job_location.lower():
                continue

            # Add the job to the filtered list
            filtered_jobs.append({
                "title": job_title,
                "company_name": company_name,
                "location": job_location,
                "remote": job_remote,
                "url": job_url
            })

        return filtered_jobs

    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        return []

# Example usage
if __name__ == "__main__":
    # Apply optional location filter and fetch remote jobs only
    location_filter = "United States"  # Replace with None for no location filter
    jobs = fetch_jobs(location=location_filter, remote_only=True)

    # Display the results
    for job in jobs:
        print(f"Title: {job['title']}")
        print(f"Company: {job['company_name']}")
        print(f"Location: {job['location']}")
        print(f"Remote: {job['remote']}")
        print(f"URL: {job['url']}")
        print("-" * 50)
