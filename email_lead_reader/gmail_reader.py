import imaplib, email
from email_lead_reader.utils import is_lead_email, extract_contacts

# 📩 Fetches unread Gmail emails and returns extracted leads
def fetch_gmail_leads(config):
    # Connect securely to Gmail's IMAP server using credentials from config
    mail = imaplib.IMAP4_SSL(config['IMAP_SERVER'], int(config['IMAP_PORT']))
    mail.login(config['EMAIL_USER'], config['EMAIL_PASS'])

    # Select the inbox
    mail.select("inbox")

    # Search for unread (UNSEEN) emails
    result, data = mail.search(None, 'UNSEEN')
    print(f"🔍 Found {len(data[0].split())} unread emails")
    # Get the first 20 email IDs
    email_ids = data[0].split()[:20]
    leads = []

    # Get whether emails should be marked as read
    mark_as_read = config.get("MARK_AS_READ", "false").lower() == "true"

    # Loop through each unread email
    for eid in email_ids:
        # Fetch full email by ID
        res, msg_data = mail.fetch(eid, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        # Extract basic details
        subject = msg["Subject"]
        sender = msg["From"]
        date = msg["Date"]

        # Extract plain text body from multipart or plain emails
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body += part.get_payload(decode=True).decode()
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode()
            except:
                continue

        # Check if subject or body contains lead-related keywords
        if is_lead_email(subject or "") or is_lead_email(body):
            # Extract contacts from body text
            emails, phones = extract_contacts(body)

            # Store in structured format
            leads.append([
                date,
                sender,
                subject,
                body[:100],
                ", ".join(emails),
                ", ".join(phones)
            ])

            # ✅ Mark as read if enabled in config
            if mark_as_read:
                mail.store(eid, '+FLAGS', '\\Seen')

    return leads
