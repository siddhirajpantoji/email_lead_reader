import csv
import os
from datetime import datetime
from email_lead_reader.gmail_reader import fetch_gmail_leads
from email_lead_reader.outlook_reader import fetch_outlook_leads

# 📄 Load configuration values from a CSV file (key,value format)
def load_config(path='config.csv'):
    config = {}
    with open(path) as f:
        for line in f:
            if "," in line:
                key, value = line.strip().split(",", 1)
                config[key.strip()] = value.strip()
    return config

# 📝 Save the extracted lead data into a timestamped CSV file inside 'output/' folder
def save_leads_csv(leads):
    # Ensure output folder exists
    os.makedirs("output", exist_ok=True)

    # Create a filename with the current timestamp
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"output/leads_{ts}.csv"

    header = [
    "Date",
    "From",
    "Subject",
    "First Name",
    "Last Name",
    "Email",
    "Company",
    "Country",
    "Services",
    "Industry",
    "Phone",
    "Referred By",
    "Referred Description",
    "Message",
    "Marketing Consent",
    "Web URL"
    ]


    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL)
        writer.writerow(header)  # header must be defined above
        writer.writerows(leads)

    print(f"✅ Saved {len(leads)} leads to {filename}")

# 🚀 Entry point: loads config, fetches leads based on provider, saves output
if __name__ == "__main__":
    config = load_config()  # Load settings like provider, credentials, etc.
    provider = config.get("EMAIL_PROVIDER", "gmail").lower()  # Default to Gmail

    # Choose email reader based on configured provider
    if provider == "gmail":
        leads = fetch_gmail_leads(config)
    elif provider == "outlook":
        leads = fetch_outlook_leads(config)
    else:
        raise Exception("Unsupported EMAIL_PROVIDER. Use 'gmail' or 'outlook'.")

    # Write the collected leads to a CSV file
    if not leads:
        print("📭 No leads found based on the search criteria.")
    else:
        print(f"📥 Found {len(leads)} leads.")
        print(leads)
        save_leads_csv(leads)
