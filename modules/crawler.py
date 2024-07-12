import requests
from bs4 import BeautifulSoup

def crawl_website(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.text
    except requests.RequestException as e:
        print(f"Error crawling {url}: {e}")
        return None

def scrape_email_from_website(url, output_file, limit, headers):
    emails = []
    # Implement your email scraping logic here
    # For example, you can use BeautifulSoup to parse the HTML
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for link in soup.find_all('a', href=True):
        link_url = link['href']
        # Check if the link is a valid URL
        if link_url.startswith('http'):
            # Crawl the link and extract emails
            link_text = crawl_website(link_url, headers)
            if link_text:
                # Extract emails from the link text
                # Implement your email extraction logic here
                # For example, you can use regular expressions
                import re
                email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                link_emails = re.findall(email_pattern, link_text)
                emails.extend(link_emails)
        if len(emails) >= limit:
            break
    return emails