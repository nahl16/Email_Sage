# Email Sage

Email Sage is a powerful email harvesting tool designed to efficiently gather and validate emails from specified websites. This tool leverages various modules for web crawling, email extraction, and validation, and dns MX records lookup.

## Features

- **Website Crawling:** Crawl specified websites to find email addresses.
- **Email Extraction:** Extract emails using pattern recognition techniques.
- **Email Validation:** Validate emails using real-time checks.
- **DNS Lookup:** Verify the existence of domains and obtain MX records.
- **User-Agent Rotation:** Rotate user agents to avoid detection while crawling.
- **Output Options:** Export results to various formats (e.g., Text, CSV, JSON, PDF).

## Installation

### Step 1: Install Python

Make sure you have Python 3.x installed on your system.

`sudo apt update`
`sudo apt install python3`

### Step 2: Install Dependencies
1.	Clone this repository:
  - `git clone https://github.com/nomanulaziz/email_sage.git`
  - `cd email_sage`
2.	Install the required dependencies:
  - `pip install -r requirements.txt`

### Step 3: Run the Application
You can run the main application using the following command:
`python email_sage.py -d [domain name]`

## Commands
To use different features of Email Sage, refer to the following commands:
-	**Crawl a Website:**
  `python email_sage.py -d [domain name] -l 5`
-	**Validate Emails:**
  `python email_sage.py -d [domain name] -v`
-	**DNS Lookup:**
  `python email_sage.py -d [domain name] –dns-lookup`
-	**Export Results (Supported Formats Text, CSV, JSON, PDF):**
  `python email_sage.py -d [domain name] -l 5 -o output.csv`
-	**Complete Scan:**
  `python email_sage.py -d [domain name] -l 5 -v –dns-lookup -o output.csv`
-	**For a full list of options, run:**
  `python email_sage.py -h`

## Graphic Interface
To use graphic interface, refer to the following commands:
`python email_sage.py -g`

<img src="GUI_EmailSage.png" width="350" height="200">

--------------
--------------
