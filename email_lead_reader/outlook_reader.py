import requests
from msal import PublicClientApplication
from email_lead_reader.parser_utils import extract_fields_from_email


# 🔐 Authenticates to Microsoft Graph using Device Flow and returns access token
def authenticate_graph(client_id, tenant_id, scopes=["Mail.ReadWrite"]):
    app = PublicClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}"
    )

    accounts = app.get_accounts()
    if accounts:
        # Try to acquire token silently if cached
        return app.acquire_token_silent(scopes, account=accounts[0])["access_token"]
    else:
        # Interactive authentication via device code
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"])  # Shows URL and code to authenticate
        return app.acquire_token_by_device_flow(flow)["access_token"]


# 📬 Fetches unread leads from Outlook inbox using Microsoft Graph API
def fetch_outlook_leads(config):
    # Authenticate and get access token
    token = authenticate_graph(config["CLIENT_ID"], config["TENANT_ID"])
    headers = {
        "Authorization": f"Bearer {token}",
        "Prefer": 'outlook.body-content-type="text"'  # Get plain text body
    }

    # 📎 Build filter query from config
    filters = ["isRead eq false"]  # Only fetch unread
    from_filter = config.get("FILTER_FROM_ADDRESS", "").strip()
    subject_filter = config.get("FILTER_SUBJECT_CONTAINS", "").strip()
    max_emails = int(config.get("MAX_EMAILS", 20))

    if from_filter:
        filters.append(f"from/emailAddress/address eq '{from_filter}'")
    if subject_filter:
        filters.append(f"contains(subject, '{subject_filter}')")

    filter_query = " and ".join(filters)

    # 📥 Graph API endpoint to read inbox messages
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages"
    params = {
        "$top": max_emails,  # Limit results
        "$filter": filter_query,
        "$select": "subject,body,receivedDateTime,from,id"
    }

    # 📡 API call to fetch emails
    response = requests.get(url, headers=headers, params=params)
    messages = response.json().get("value", [])

    if not messages:
        print("📭 No unread emails found based on the search criteria.")
        return []

    leads = []

    # 🧠 Parse each email and extract lead data
    for msg in messages:
        sender = msg.get("from", {}).get("emailAddress", {}).get("address", "")
        subject = msg.get("subject", "")
        body = msg.get("body", {}).get("content", "")
        date = msg.get("receivedDateTime", "")

        # Extract fields using helper function
        fields = extract_fields_from_email(body)

        # Append structured lead to list
        leads.append([
            date,
            sender,
            subject,
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
            fields["message"],  # Truncate to avoid overflow
            fields["marketing_consent"],
            fields["web_url"],
            fields["validation_result"]
        ])

        # ✅ Mark email as read if configured
        if config.get("MARK_AS_READ", "").lower() == "true":
            message_id = msg["id"]
            patch_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
            requests.patch(patch_url, headers=headers, json={"isRead": True})

    return leads
