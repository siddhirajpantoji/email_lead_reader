import requests
from msal import PublicClientApplication
from email_lead_reader.parser_utils import extract_fields_from_email 

def authenticate_graph(client_id, tenant_id, scopes=["Mail.ReadWrite"]):
    app = PublicClientApplication(client_id, authority=f"https://login.microsoftonline.com/{tenant_id}")
    accounts = app.get_accounts()
    if accounts:
        return app.acquire_token_silent(scopes, account=accounts[0])["access_token"]
    else:
        flow = app.initiate_device_flow(scopes=scopes)
        print(flow["message"])
        return app.acquire_token_by_device_flow(flow)["access_token"]

def fetch_outlook_leads(config):
    token = authenticate_graph(config["CLIENT_ID"], config["TENANT_ID"])
    headers = {
        "Authorization": f"Bearer {token}",
        "Prefer": 'outlook.body-content-type="text"'
    }

    sender_filter = config.get("SENDER", "").strip()
    filter_query = "isRead eq false"

    from_filter = config.get("FILTER_FROM_ADDRESS", "").strip()
    subject_keyword = config.get("FILTER_SUBJECT_CONTAINS", "").strip()
    top_n = int(config.get("MAX_EMAILS", 20))

    filters = ["isRead eq false"]
    if from_filter:
        filters.append(f"from/emailAddress/address eq '{from_filter}'")
    if subject_keyword:
        filters.append(f"contains(subject, '{subject_keyword}')")

    filter_query = " and ".join(filters)

    max_emails = int(config.get("MAX_EMAILS", 20))

    url = "https://graph.microsoft.com/v1.0/me/mailFolders/Inbox/messages"
    params = {
        "$top": max_emails,
        "$filter": filter_query,
        "$select": "subject,body,receivedDateTime,from,id"
    }

    resp = requests.get(url, headers=headers, params=params)
    messages = resp.json().get("value", [])

    if not messages:
        print("No unread emails found based on the search criteria.")
        return []

    leads = []
    for msg in messages:
        sender = msg["from"]["emailAddress"]["address"]
        subject = msg["subject"]
        body = msg["body"]["content"][:500]
        date = msg["receivedDateTime"]

        fields = extract_fields_from_email(body)
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
            fields["message"][:1000],
            fields["marketing_consent"],
            fields["web_url"]
        ])
        if config.get("MARK_AS_READ", "").lower() == "true":
            message_id = msg["id"]
            patch_url = f"https://graph.microsoft.com/v1.0/me/messages/{message_id}"
            requests.patch(patch_url, headers=headers, json={"isRead": True})

    return leads
