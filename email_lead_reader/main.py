import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
import os
import csv
import re

# Load environment variables
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
IMAP_SERVER = os.getenv("IMAP_SERVER", "imap.gmail.com")
IMAP_PORT = int(os.getenv("IMAP_PORT", 993))
CSV_FILE = "leads.csv"

def decode_mime_words(s):
    try:
        decoded = decode_header(s)
        parts = []
        for part, enc in decoded:
            if isinstance(part, bytes):
                try:
                    part = part.decode(enc or "utf-8", errors="ignore")
                except:
                    part = part.decode("utf-8", errors="ignore")
            parts.append(part)
        return " ".join(parts)
    except:
        return s

def extract_contact_info(body_text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", body_text)
    phones = re.findall(r"\+?\d[\d\s\-\(\)]{7,}\d", body_text)
    return ", ".join(set(emails)), ", ".join(set(phones))

def is_lead_email(subject, body):
    lead_keywords = [
        "lead", "inquiry", "interested", "contact", "requirement",
        "demo", "project", "looking for", "need", "proposal", "quote", "rfp", "business"
    ]
    content = (subject + " " + body).lower()
    return any(keyword in content for keyword in lead_keywords)

def connect_to_mailbox():
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL_USER, EMAIL_PASS)
    return mail

def save_to_csv(data: list):
    file_exists = os.path.isfile(CSV_FILE)
    with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["Date", "From", "Subject", "Body", "Emails", "Phones"])
        if not file_exists:
            writer.writeheader()
        for row in data:
            writer.writerow(row)

def read_unread_emails(mail):
    mail.select("inbox")
    status, messages = mail.search(None, "UNSEEN")
    email_ids = messages[0].split()
    latest_ids = email_ids[-20:] if len(email_ids) > 20 else email_ids

    print(f"📬 Found {len(email_ids)} unread emails.\n")

    results = []

    for e_id in latest_ids:
        res, msg_data = mail.fetch(e_id, "(RFC822)")  # Fetch full email and mark as read
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])

                subject = decode_mime_words(msg.get("Subject", ""))
                sender = decode_mime_words(msg.get("From", ""))
                date = msg.get("Date")

                # Extract body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and "attachment" not in str(part.get("Content-Disposition", "")):
                            try:
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                            except:
                                continue
                            break
                else:
                    try:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    except:
                        body = ""

                if is_lead_email(subject, body):
                    email_list, phone_list = extract_contact_info(body)
                    results.append({
                        "Date": date,
                        "From": sender,
                        "Subject": subject,
                        "Body": body.strip()[:200],
                        "Emails": email_list,
                        "Phones": phone_list
                    })
                    print(f"🎯 LEAD: {sender} | {subject}")
                else:
                    print(f"⏩ Skipped: {subject}")

        # ✅ Mark email as read explicitly (redundant, but safe)
        mail.store(e_id, '+FLAGS', '\\Seen')
        print(f"📥 Processed email ID: {e_id.decode('utf-8')}")
        print("results so far:", len(results))

    if results:
        save_to_csv(results)
        print(f"\n✅ Saved {len(results)} leads to {CSV_FILE}")
    else:
        print("📭 No lead emails found.")

def main():
    try:
        mail = connect_to_mailbox()
        read_unread_emails(mail)
        mail.logout()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
