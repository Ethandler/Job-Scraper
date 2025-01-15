# Job Scraper

## Overview
This project is an automated job search tool that fetches job listings from the **Arbeitnow Job Board API**. It filters and displays jobs based on user-defined criteria, such as location and remote status. The tool is designed to streamline job searching for developers and other professionals.

---

## Features
- Fetches job listings directly from the **Arbeitnow API**.
- Filters jobs by:
  - Location (e.g., "United States").
  - Remote-only roles.
- Outputs job details, including:
  - Job Title
  - Company Name
  - Location
  - Remote Status
  - URL to apply.
- Can be extended with additional features like saving results to a file or displaying data in a GUI.

---

## Prerequisites
Before you begin, ensure you have the following installed:
- **Python 3.6 or later**
- `requests` library: Install via pip:
  ```bash
  pip install requests
  ```

---

## Installation
1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/job-scraper.git
   ```
2. Navigate to the project directory:
   ```bash
   cd job-scraper
   ```
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Add a `requirements.txt` with `requests` if needed.)*

---

## Usage
1. Open the `scraper.py` file and customize the filters:
   - Change `location_filter` to your desired location or set it to `None` for no filtering.
   - Adjust `remote_only` to `True` for remote jobs only, or `False` for all jobs.
2. Run the script:
   ```bash
   python scraper.py
   ```
3. View the results in the terminal.

---

## Example Output
```
Title: Software Engineer
Company: Example Corp
Location: United States
Remote: True
URL: https://example.com/job/software-engineer
--------------------------------------------------
```

---

## Future Enhancements
- Add a graphical user interface (GUI) for better user experience.
- Include options to save results to a file (CSV/JSON).
- Add support for multiple APIs or job boards.

---

## Contributing
Contributions are welcome! Feel free to submit issues or pull requests for improvements.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Thanks to the [Arbeitnow API](https://arbeitnow.com/api/job-board-api) for providing free access to job listings.
