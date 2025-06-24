# 📧 Lead Extraction from Gmail Inbox using IMAP

This Python script connects to your Gmail inbox via IMAP, reads unread emails, filters **lead-related emails**, extracts **contact information (emails, phone numbers)** from the body, and stores the results into a local CSV file (`leads.csv`).

---

## 🧠 Ideation
* [Ideation PPT](./ideation-ppt.md)
* [Ideation Document](./ideation.md)


## ✅ Features

* Connects securely to Gmail using IMAP
* Reads **only unread** emails (doesn't mark them read)
* Filters emails using lead-related **keywords**
* Extracts contact data:

  * Email addresses
  * Phone numbers
* Saves extracted information to `leads.csv`
* Credentials are stored safely in a `.env` file

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
EMAIL_PROVIDER,gmail                # or "outlook"
EMAIL_USER,your_email@gmail.com
EMAIL_PASS,your_gmail_app_password
IMAP_SERVER,imap.gmail.com
IMAP_PORT,993
CLIENT_ID,xxxxxx-your-outlook-id
TENANT_ID,xxxxxx-your-tenant-id
MARK_AS_READ,true                  # or false
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
* Read up to 20 unread emails
* Filter for leads
* Save them to: `output/leads_YYYY-MM-DD_HH-MM.csv`
* Mark emails as read (optional via config)

---

## 🧐 Lead Detection Logic

The script detects lead emails if:

* The **subject** or **body** contains keywords like:

  * `"lead"`, `"inquiry"`, `"interested"`, `"contact"`, `"requirement"`, `"demo"`, `"project"`, `"need"`, `"proposal"`, `"quote"`, etc.

---

## 📄 Output Format: `leads.csv`

| Date                            | From                                                 | Subject               | Body                             | Emails                                      | Phones         |
| ------------------------------- | ---------------------------------------------------- | --------------------- | -------------------------------- | ------------------------------------------- | -------------- |
| Mon, 17 Jun 2024 11:00:00 +0000 | John Doe [john@example.com](mailto:john@example.com) | Inquiry about website | Hi, I'm looking for a website... | [john@example.com](mailto:john@example.com) | +91 9876543210 |

---

## 🧙‍♂️ File Structure

```
email_lead_reader/
├── email_lead_reader/         # Source code package
│   ├── __init__.py
│   └── main.py                # Your main script
├── tests/                     # Unit tests
│   └── test_main.py
├── .gitignore
├── requirements.txt
├── README.md
├── setup.py                   # For packaging
└── venv/                      # Virtual environment (optional, local only)
```

---

## ✨ Possible Upgrades

You can easily extend this script to:


* **LinkedIn API** integration to fetch company/individual profiles associated with emails and enrich the data 
* **AI tools** for analyzing and scoring leads based on their context, sentiment, or frequency 
* Filter by **date range** (e.g. only this week)
* Process **specific Gmail labels** or **specific Gmail labels**
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
