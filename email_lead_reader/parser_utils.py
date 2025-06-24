import re


def clean_multiline(text):
    return text.replace("\r", "").replace("\n", "\t").strip()


def extract_fields_from_email(body):
    def extract_field(key, multiline=False):
        pattern = rf"{re.escape(key)}\s*:\s*(.*)"
        match = re.search(pattern, body, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return ""

    # Get message content after "Message:" and preserve line breaks if needed
    message_start = re.search(r"Message:\s*", body, re.IGNORECASE)
    message = ""
    if message_start:
        message = body[message_start.end():].strip()

    return {
        "first_name": extract_field("First Name"),
        "last_name": extract_field("Last Name"),
        "email": extract_field("Email Address"),
        "company": extract_field("Company Name"),
        "country": extract_field("Country"),
        "services": extract_field("Services/Technologies interested in"),
        "industry": extract_field("Industry"),
        "phone": extract_field("Phone Number"),
        "referred_by": extract_field("Referred by"),
        "referred_description": clean_multiline(extract_field("Referred by Description")),
        "message": clean_multiline(message),
        "marketing_consent": extract_field("Marketing Consent"),
        "web_url": extract_field("Email Address").split("@")[-1] if "@" in extract_field("Email Address") else "",
    }

