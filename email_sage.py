import sys
import argparse
import time
from urllib.parse import urlparse
import json
import csv
from fpdf import FPDF
from PyQt5.QtWidgets import QApplication

from modules.email_validator import EmailValidator
from user_agent_rotator import UserAgentRotator
import pyfiglet

from modules.dns_lookup import dns_lookup_mx
from modules.crawler import crawl_website, scrape_email_from_website
from modules.pattern_recognition import extract_emails
from email_filters import filter_emails, filter_duplicates, filter_invalid_emails

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15",
    "Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/605.1.15",
]

def get_random_user_agent():
    """Returns a random User-Agent string from the list."""
    user_agent_rotator = UserAgentRotator()  # Create a UserAgentRotator instance
    return user_agent_rotator.get_random_user_agent()

# for displaying name
def print_banner():
    banner = pyfiglet.figlet_format("Email Sage")
    print(banner)

def save_results(emails, output_file, validation_results=None, mx_records=None):
    file_extension = output_file.split('.')[-1]
    
    if file_extension == 'txt':
        with open(output_file, 'w') as f:
            f.write("Emails:\n")
            for email in emails:
                f.write(email + '\n')
            if validation_results:
                f.write("\nValidation Results:\n")
                for result in validation_results:
                    f.write(f"{result['email']}: {result['status']}\n")
            if mx_records:
                f.write("\nMX Records:\n")
                for record in mx_records:
                    f.write(record + '\n')
    elif file_extension == 'csv':
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Email"])
            for email in emails:
                writer.writerow([email])
            if validation_results:
                writer.writerow([])
                writer.writerow(["Validation Results"])
                writer.writerow(["Email", "Status"])
                for result in validation_results:
                    writer.writerow([result['email'], result['status']])
            if mx_records:
                writer.writerow([])
                writer.writerow(["MX Records"])
                for record in mx_records:
                    writer.writerow([record])
    elif file_extension == 'json':
        results = {"emails": emails}
        if validation_results:
            results["validation_results"] = validation_results
        if mx_records:
            results["mx_records"] = mx_records
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=4)
    elif file_extension == 'pdf':
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="Emails:", ln=True)
        for email in emails:
            pdf.cell(200, 10, txt=email, ln=True)
        if validation_results:
            pdf.cell(200, 10, txt="Validation Results:", ln=True)
            for result in validation_results:
                pdf.cell(200, 10, txt=f"{result['email']}: {result['status']}", ln=True)
        if mx_records:
            pdf.cell(200, 10, txt="MX Records:", ln=True)
            for record in mx_records:
                pdf.cell(200, 10, txt=record, ln=True)
        pdf.output(output_file)
    else:
        print(f"Unsupported file format: {file_extension}. Supported formats are txt, csv, json, and pdf.")

def main(args=None):
    print_banner()
    parser = argparse.ArgumentParser(description='Email Sage Tool',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-d', '--domain', help='Company name or domain to search')
    parser.add_argument('-l', '--limit', type=int, default=10, help='Limit the number of search results per link')
    parser.add_argument('-o', '--output', help='Output file to save emails')
    parser.add_argument('-v', '--validate', action='store_true', default=False,
                        help='Enable email validation using regular expressions')
    parser.add_argument('--dns-lookup', action='store_true', default=False,
                        help='Perform DNS lookup to check for MX records (optional)')
    parser.add_argument('-g', '--gui', action='store_true', default=False, help='Launch GUI')

    args = parser.parse_args(args)

    if args.gui:
        from gui import EmailFinderApp
        app = QApplication(sys.argv)
        ex = EmailFinderApp()
        ex.show()
        sys.exit(app.exec_())

    if not args.domain:
        print("Domain is required. Use -d or --domain to specify the domain.")
        sys.exit(1)

    start_time = time.time()

    # Parse the domain to get the scheme (http/https)
    parsed_url = urlparse(args.domain)
    if parsed_url.scheme:
        domain_url = parsed_url.scheme + '://' + parsed_url.netloc
    else:
        domain_url = 'https://' + args.domain  # Assuming https by default if no scheme is provided

    try:
        # Crawl the main website
        print("Crawling main website:")
        headers = {'User-Agent': get_random_user_agent()}
        text = crawl_website(domain_url, headers)
        if text:
            # Extract emails from the main website
            emails = extract_emails(text)
            if emails:
                print("Emails found on main page:")
                for email in emails:
                    print(email)
            else:
                print("\nNo emails found on main page")

            # Scrape emails from additional links within the website
            print("\nScraping emails from additional links:")
            additional_emails = scrape_email_from_website(domain_url, args.output, limit=args.limit, headers=headers)
            if additional_emails:
                print("\nEmails found on additional links:")
                for email in additional_emails:
                    print(email)
            else:
                print("\nNo emails found on additional links")

            # Combine, deduplicate, and filter emails
            all_emails = list(emails + additional_emails)
            print("\n" + f"Combined email list: {all_emails}")
            all_emails = filter_duplicates(all_emails)
            all_emails = filter_emails(all_emails)
            filtered_emails = filter_invalid_emails(all_emails)

            validation_results = []
            if args.validate:
                print("\nStarting to check Email Deliverability")
                validator = EmailValidator(
                    api_key="live_91584f2b89e222a4042423aa9fac2eb3428cca329ffa1a33308964881ae0869f")  # Create validator for verification with --validate
                for email in filtered_emails:
                    deliverable = validator.is_valid_deliverable(email)
                    if deliverable is not None:
                        validation_results.append({
                            "email": email,
                            "status": "deliverable" if deliverable else "undeliverable"
                        })
                        print(f"{email} is likely {'deliverable' if deliverable else 'undeliverable'}.")

            mx_records = None
            if args.dns_lookup:
                try:
                    mx_records = dns_lookup_mx(args.domain.strip())  # Check for MX records
                    if mx_records:
                        print(f"\nMX Records found: {mx_records}")
                    else:
                        print(f"\nNo MX Records found")
                except Exception as e:
                    print(f"Error performing DNS lookup: {e}")

            # Save results to output file if specified
            if args.output:
                save_results(filtered_emails, args.output, validation_results, mx_records)

        else:
            print("\nNo data retrieved from crawling.")

    except Exception as e:
        print(f"Error crawling {args.domain}: {e}")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"\nTotal execution time: {elapsed_time:.2f} seconds")

if __name__ == '__main__':
    main()
