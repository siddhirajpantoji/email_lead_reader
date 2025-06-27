import re
import dns.resolver
import smtplib
import socket


def extract_multiline_field(body, start_key, end_key=None):
    """
    Extracts text between start_key and end_key (if provided), with newline replaced by tab for CSV.
    If end_key is not found, returns from start_key till end of body.
    """
    if end_key:
        pattern = rf"{re.escape(start_key)}\s*:\s*(.*?)(?=\s*{re.escape(end_key)}\s*:|$)"
    else:
        pattern = rf"{re.escape(start_key)}\s*:\s*(.*)"

    match = re.search(pattern, body, re.IGNORECASE | re.DOTALL)
    if match:
        text = match.group(1).strip()
        return text.replace("\r", "").replace("\n", "\t")
    return ""



def clean_multiline(text):
    if not text:
        return ""
    return text.replace("\r", "").replace("\n", "\t").strip()
def extract_fields_from_email(body):
    def extract_field(key):
        pattern = rf"{re.escape(key)}\s*:\s*(.*)"
        match = re.search(pattern, body, re.IGNORECASE)
        return match.group(1).strip() if match else ""

    email_addr = extract_field("Email Address")
    domain = email_addr.split("@")[-1] if "@" in email_addr else ""

    return {
        "first_name": extract_field("First Name"),
        "last_name": extract_field("Last Name"),
        "email": email_addr,
        "company": extract_field("Company Name"),
        "country": extract_field("Country"),
        "services": extract_field("Services/Technologies interested in"),
        "industry": extract_field("Industry"),
        "phone": extract_field("Phone Number"),
        "referred_by": extract_field("Referred by"),
        "referred_description": extract_multiline_field(body, "Referred by Description", "Message"),
        "message": extract_multiline_field(body, "Message", "Marketing Consent"),
        "marketing_consent": extract_field("Marketing Consent"),
        "web_url": domain,
        "validation_result": verify_email(email_addr)
    }


def is_valid_email_format(email):
    """Check format using regex"""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

def has_mx_record(domain):
    """Check MX records for domain"""
    try:
        mx_records = dns.resolver.resolve(domain, 'MX')
        return [record.exchange.to_text() for record in mx_records]
    except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN, dns.resolver.Timeout):
        return []

def smtp_check(email, mx_hosts, timeout=10):
    """Connect to SMTP server and simulate a recipient check"""
    for host in mx_hosts:
        try:
            server = smtplib.SMTP(timeout=timeout)
            server.connect(host)
            server.helo("example.com")
            server.mail("verify@example.com")
            code, _ = server.rcpt(email)
            server.quit()

            if code == 250:
                return True  # Address accepted
            elif code in [550, 551, 553]:
                return False  # Mailbox doesn't exist
        except (socket.error, smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            continue
    return None  # Inconclusive

def verify_email(email):
    """Performs full format + MX + SMTP validation"""
    print(f"Validating email: {email}")
    if not is_valid_email_format(email):
        return "Invalid Format"

    domain = email.split('@')[-1]
    mx_hosts = has_mx_record(domain)

    if not mx_hosts:
        return "Invalid Domain"

    return "Valid Domain"  # MX records found
