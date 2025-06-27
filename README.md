# 📧 Lead Extraction from Gmail Inbox using IMAP

This Python tool connects to your **Gmail** or **Outlook** inbox, reads unread emails, filters **lead-related messages**, extracts structured contact information, and saves it into a timestamped CSV file inside the `output/` folder.

---

## 🧠 Ideation
* [Ideation PPT](./ideation-ppt.md)
* [Ideation Document](./ideation.md)


## ✅ Features

* 🔐 Reads **Gmail (via IMAP)** or **Outlook (via Microsoft Graph API)**
* 🔍 Filters based on sender & subject keywords (from `config.csv`)
* 📋 Extracts structured fields: name, email, phone, company, message, etc.
* 📁 Saves results in: `output/leads_YYYY-MM-DD_HH-MM.csv`
* ⚙️ Configurable max email count (`MAX_EMAILS`) & read status (`MARK_AS_READ`)
* 🧪 Lightweight, CLI-based and easy to extend
* 🧠 Intelligent parsing using regex
* 📝 Uses a simple `config.csv`  for credentials
* ⚙️ Optional `MARK_AS_READ=true` toggle to control if emails should be marked as read

---

## 🛠 Requirements

* Python 3.7+
* Gmail account (IMAP access enabled) OR Outlook account with Azure App credentials
* Internet access

---

## 🎞 Installation

### 1. Clone the Repo or Copy Script

```bash
git clone https://github.com/siddhirajpantoji/email_lead_reader.git
cd email_lead_reader
```

### 2. Create Virtual Environment (Optional but Recommended)

```bash
python3 -m venv venv
source venv/bin/activate
# On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you don’t have `requirements.txt`, just run:

```bash
pip install python-dotenv
```

---

## 🔐 Setup: Create a file `config.csv` in the root folder:

```csv
key,value
EMAIL_PROVIDER,gmail
EMAIL_USER,your_email@gmail.com
EMAIL_PASS,your_gmail_app_password
IMAP_SERVER,imap.gmail.com
IMAP_PORT,993
CLIENT_ID,your_outlook_client_id
TENANT_ID,your_outlook_tenant_id
FILTER_FROM_ADDRESS,noreply@form.com
FILTER_SUBJECT_CONTAINS,Notification
MAX_EMAILS,25
MARK_AS_READ,true
```

🔒 If using Gmail with 2-Step Verification:
→ [Create an App Password](https://myaccount.google.com/apppasswords)

🔑 If using Outlook:
→ Register an app at [Azure Portal](https://portal.azure.com/) and get `CLIENT_ID` & `TENANT_ID`.

---

## 🚀 How to Run

From the root folder:

```bash
python -m email_lead_reader.main
```

This will:

* Connect to Gmail or Outlook (based on config)
* Mark emails as read (optional via config)
* Read up to `MAX_EMAILS` unread messages
* Filter by `FROM` and/or subject keyword
* Extract form submission fields
* Save results to `output/leads_YYYY-MM-DD_HH-MM.csv`
* Optionally mark emails as read based on config

---


## 📄 Extracted Fields (CSV)

| Date                            | From                                                           | Subject                     | First Name | Last Name | Email                                                         | Company        | Country       | Services         | Industry                     | Phone           | Referred By | Referred Description    | Message                                                                                                                                      | Marketing Consent | Web URL          |
| ------------------------------- | -------------------------------------------------------------- | --------------------------- | ---------- | --------- | ------------------------------------------------------------- | -------------- | ------------- | ---------------- | ---------------------------- | --------------- | ----------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------- | ---------------- |
| Wed, 25 Jun 2025 00:43:32 +0530 | John Smith [jsmith@formsubmit.io](mailto:jsmith@formsubmit.io) | Form Submittal Notification | Chad       | Hudgins   | [chudgins@advanceddata.com](mailto:chudgins@advanceddata.com) | Advanced Data  | United States | Customer Success | Banking & Financial Services | 8005370458      | Others      |                         | We are trying to do an urgent employment verification for one of your employees on behalf of Provident Bank. Please respond with HR contact. | 1                 | advanceddata.com |
| Tue, 24 Jun 2025 13:15:00 +0530 | Jane Doe [jane@solutions.com](mailto:jane@solutions.com)       | Inquiry - Software Support  | Jane       | Doe       | [jane@solutions.com](mailto:jane@solutions.com)               | Tech Solutions | Canada        | Software Support | IT Services                  | +1-416-555-1234 | Google      | Referred by SEO search. | I need information on your software products and pricing.                                                                                    | Yes               | solutions.com    |

---

## 🧙‍♂️ File Structure

```
email_lead_reader/
├── email_lead_reader/
│   ├── gmail_reader.py         # Gmail IMAP logic
│   ├── outlook_reader.py       # Microsoft Graph logic
│   ├── parser_utils.py         # Email field extraction logic
│   └── main.py                 # Main launcher
├── config.csv                  # Email credentials & filters
├── output/                     # All output CSV files
├── requirements.txt            # Required libraries
├── README.md                   # You're here
└── venv/                       # Virtual environment (optional, local only)
```

---

## ✨ Possible Upgrades

You can easily extend this script to:


* **LinkedIn API** integration to fetch company/individual profiles associated with emails and enrich the data 
* **AI tools** for analyzing and scoring leads based on their context, sentiment, or frequency 
* Filter by **date range** (e.g. only this week)
* Process **specific Gmail labels** or **specific Outlook labels**
* Push leads to **Google Sheets** or a CRM
* Add a **dashboard** to visualize leads
* Use **AI** to suggest lead scores or categorize leads
* Integrate with **Slack or CRM**

Let me know and I’ll help you build these too!

---

## 📢 Questions?

Open an issue or message **Siddhiraj Pantoji**.
📧 Email: [siddhirajpantoji@gmail.com](mailto:siddhirajpantoji@gmail.com)
🔗 Connect via [LinkedIn](https://www.linkedin.com/in/siddhiraj-pantoji/) or [visit the portfolio](https://siddhirajpantoji.github.io/).
