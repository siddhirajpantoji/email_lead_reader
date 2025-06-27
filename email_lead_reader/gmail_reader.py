import imaplib
import email
from email_lead_reader.parser_utils import extract_fields_from_email 

def fetch_gmail_leads(config):
    # Establish secure IMAP connection
    mail = imaplib.IMAP4_SSL(config['IMAP_SERVER'], int(config['IMAP_PORT']))
    mail.login(config['EMAIL_USER'], config['EMAIL_PASS'])
    mail.select("inbox")

    # Build IMAP search query
    from_filter = config.get("FILTER_FROM_ADDRESS", "").strip()
    subject_keyword = config.get("FILTER_SUBJECT_CONTAINS", "").strip()

    search_parts = ['UNSEEN']
    if from_filter:
        search_parts.append(f'FROM "{from_filter}"')
    if subject_keyword:
        search_parts.append(f'SUBJECT "{subject_keyword}"')

    search_criteria = f'({" ".join(search_parts)})'

    result, data = mail.search(None, search_criteria)
    email_ids = data[0].split()
    print(f"📥 Found {len(email_ids)} unread emails based on the search criteria.")
    max_emails = int(config.get("MAX_EMAILS", 20))

    if not email_ids:
        print("📭 No unread emails found based on the search criteria.")
        return []

    leads = []

    for eid in email_ids[:max_emails]:
        # Fetch full email data
        res, msg_data = mail.fetch(eid, "(BODY.PEEK[])")
        if res != 'OK':
            print(f"❌ Failed to fetch email {eid.decode()}")
            continue
        msg = email.message_from_bytes(msg_data[0][1])

        # Extract metadata
        subject = msg["Subject"]
        sender = msg["From"]
        date = msg["Date"]

        # Decode message body
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

        fields = extract_fields_from_email(body)
        print(fields)
        leads.append([
            date, sender, subject,
            fields["first_name"],
            fields["last_name"],
            fields["email"],
            fields["company"],
            fields["country"],
            fields["services"],
            fields["industry"],
            fields["phone"],
            fields["referred_by"],
            fields["referred_description"],
            fields["message"],
            fields["marketing_consent"],
            fields["web_url"],
            fields["validation_result"]  # Validation result of the email
        ])

        # Optional: Mark as read based on config
        print(config.get("MARK_AS_READ", "").lower())
        if config.get("MARK_AS_READ", "").lower() == "true":
            print(f"✅ Marking email {eid.decode()} as read")
            mail.store(eid, '+FLAGS', '\\Seen')
        else:
            print(f"❌ Not marking email {eid.decode()} as read")

    return leads
