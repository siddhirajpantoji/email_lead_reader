import re

KEYWORDS = ["lead", "inquiry", "interested", "contact", "requirement", "demo", "project", "need", "proposal", "quote"]

def is_lead_email(text):
    return any(k.lower() in text.lower() for k in KEYWORDS)

def extract_contacts(text):
    emails = re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', text)
    phones = re.findall(r'\+?\d[\d\-\s]{8,}\d', text)
    return list(set(emails)), list(set(phones))
