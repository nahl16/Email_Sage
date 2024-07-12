import kickbox
import re


class EmailValidator:
    """
    Validates email addresses using regular expressions and optionally with Kickbox API.
    """

    def __init__(self, api_key=None):
        """
        Initializes the validator.

        Args:
            api_key (str, optional): Your Kickbox API key for enhanced validation. Defaults to None.
        """
        self.regex = r"(^[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+(\.[-!#$%&'*+/=?^_`{|}~a-zA-Z0-9]+)*@[a-zA-Z0-9]([-a-zA-Z0-9]{0,61}[a-zA-Z0-9])?\.[a-zA-Z]{2,}$)"
        self.kickbox_api_key = api_key

    def is_valid_deliverable(self, email):
        """
        Validates email deliverability using Kickbox API (if API key provided).

        Args:
            email (str): The email address to validate.

        Returns:
            bool: True if the email is likely deliverable, False otherwise (or None if Kickbox unavailable).
        """
        if self.kickbox_api_key:
            try:
                deliverable = is_email_address_valid(email, self.kickbox_api_key)
                print(f"Deliverability check for {email}: {deliverable}")
                return deliverable
            except Exception as e:
                print(f"Error using Kickbox API: {e}")
                return None
        else:
            print("Warning: Kickbox API not provided for deliverability check.")
            return None


def is_email_address_valid(email, api_key):
    """
    Helper function to perform Kickbox verification (used internally and for standalone usage).

    Args:
        email (str): The email address to validate.
        api_key (str): Your Kickbox API key.

    Returns:
        bool: True if the email is likely deliverable, False otherwise.
    """
    # Initialize Kickbox client with the provided API key
    client = kickbox.Client(api_key)
    kbx = client.kickbox()

    # Send the email for verification
    response = kbx.verify(email)

    # Return True if deliverable, False if undeliverable
    return response.body['result'] != "undeliverable"
