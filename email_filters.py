from email_validator import validate_email
def filter_emails(emails):
    """Filters out potentially invalid emails based on simple heuristics."""
    print("\nStarting to filter emails for basic structure validation.")
    valid_emails = []
    for email in emails:
        if "@" in email and "." in email:
            valid_emails.append(email)
    print(f"Valid emails after basic validation: {valid_emails}")
    return valid_emails

def filter_duplicates(emails):
    """Removes duplicate emails."""
    print("\nStarting to remove duplicate emails.")
    unique_emails = list(set(emails))
    print(f"Emails after removing duplicates: {unique_emails}")
    return unique_emails

def filter_invalid_emails(emails, invalid_emails=None):
    """Filters out specific invalid emails from the list."""
    if invalid_emails is None:
        invalid_emails = ['example@example.com', 'info@example.com', 'support@example.com']  # default invalid emails
    print("\nStarting to filter out specific invalid emails.")
    filtered_emails = [email for email in emails if email not in invalid_emails]
    print(f"Emails after filtering invalid emails: {filtered_emails}")
    return filtered_emails
