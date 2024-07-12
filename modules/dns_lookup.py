import subprocess


def dns_lookup_mx(domain):
    try:
        # Execute dig command to retrieve MX records
        result = subprocess.run(['dig', 'MX', '+short', domain], capture_output=True, text=True, check=True)
        mx_records = result.stdout.strip().splitlines()
        return mx_records
    except subprocess.CalledProcessError as e:
        # Handle specific error codes
        if e.returncode == 10:
            print(f"No MX Records found for {domain}")
            return []
        else:
            print(f"Error executing dig command: {e}")
            return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        return []
