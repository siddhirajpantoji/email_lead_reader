import requests
from msal import PublicClientApplication
from email_lead_reader.utils import is_lead_email, extract_contacts

# 🔐 Handles Microsoft Graph API auth using device code flow
def authenticate_graph(client_id, tenant_id, scopes=["Mail.ReadWrite"]):
    # Create a public app with your Azure AD client and tenant ID
    app = PublicClientApplication(
        client_id,
        authority=f"https://login.microsoftonline.com/{tenant_id}"
    )

    # Try to use an existing session
    accounts = app.get_accounts()
    if accounts:
        return app.acquire_token_silent(scopes, account=accounts[0])["access_token"]
    else:
        # Fall back to device login flow
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"])  # Shows user instructions
        return app.acquire_token_by_device_flow(flow)["access_token"]

# 📥 Fetches unread emails from Outlook and extracts lead details
def fetch_outlook_leads(config):
    # Authenticate and get token
    token = authenticate_graph(config["CLIENT_ID"], config["TENANT_ID"])

    # Set auth and preference headers
    headers = {
        "Authorization": f"Bearer {token}",
        "Prefer": 'outlook.body-content-type="text"',
        "Content-Type": "application/json"
    }

    # Query unread messages (top 20) from the Inbox
    url = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages"
    params = {
        "$top": 20,
        "$filter": "isRead eq false",
        "$select": "id,subject,body,receivedDateTime,from"
    }

    # Send request to Microsoft Graph
    resp = requests.get(url, headers=headers, params=params)
    messages = resp.json().get("value", [])
    leads = []

    # Check if config allows marking emails as read
    mark_as_read = config.get("MARK_AS_READ", "false").lower() == "true"

    for msg in messages:
        sender = msg["from"]["emailAddress"]["address"]
        subject = msg["subject"]
        body = msg["body"]["content"][:500]
        date = msg["receivedDateTime"]

        # Check if this email is a potential lead
        if is_lead_email(subject or "") or is_lead_email(body):
            emails, phones = extract_contacts(body)
            leads.append([
                date,
                sender,
                subject,
                body[:100],
                ", ".join(emails),
                ", ".join(phones)
            ])

            # ✅ Mark email as read using PATCH request
            if mark_as_read:
                mark_read_url = f"https://graph.microsoft.com/v1.0/me/messages/{msg['id']}"
                requests.patch(mark_read_url, headers=headers, json={"isRead": True})

    return leads
