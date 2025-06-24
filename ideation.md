# 🧠 Ideation Document: Email Lead Extractor

## 📌 Title of Idea

**Email Lead Extractor**
A simple automation tool that helps businesses extract and organize leads directly from their inbox.

---

## 🎯 Problem Statement

We receive potential customer leads directly through email. However, identifying, filtering, and organizing these leads manually is time-consuming and inefficient. Important leads can be easily missed, especially when the inbox is cluttered.

This causes:

* Loss of potential customers
* Delays in follow-up communication
* Poor or no integration with CRM systems

---

## 💡 Proposed Solution

The solution is a Python-based script that automatically:

* Connects to your Gmail inbox via IMAP or Microsoft Outlook via Graph API
* Searches for emails containing lead-related content using pre-defined keywords
* Extracts important contact information like phone numbers and email addresses
* Stores the information into a structured CSV file with a timestamp inside an `/output` directory

This tool provides a hands-free experience for converting unstructured email data into structured, actionable sales leads.

---

## 👥 Target Audience

This script is designed for:

* Marketing and sales teams that want to automate lead organization
* CRM administrators looking for lightweight integrations

---

## 🛠️ Core Features

* **Secure Gmail (IMAP) and Outlook (Graph API)** access
* **Keyword-based lead detection** from email subject and body
* **Extraction of phone numbers and email addresses** using pattern matching
* **CSV file output** stored in `/output` with timestamps
* **Configurable options via `config.csv`**, including toggle for `MARK_AS_READ`
* Lightweight, modular, and easily customizable

---

## 🧪 Minimum Viable Product (MVP)

The MVP version of this script includes:

* Reading 20 unread emails from the Gmail or Outlook inbox
* Filtering them using predefined keywords like “lead”, “inquiry”, “requirement”
* Extracting any email addresses or phone numbers present
* Writing the results to a CSV file in the `/output` folder
* Ability to mark emails as read based on `config.csv`

---

## 📊 Competitor Analysis

| Tool          | Pros                | Cons                     |
| ------------- | ------------------- | ------------------------ |
| Zapier        | Easy automation     | Expensive at scale       |
| Mailparser.io | Powerful, flexible  | Paid-only, complex setup |
| Our Solution  | Lightweight, simple | CLI only (no UI yet)     |

---

## 📈 Success Metrics

To evaluate the success of this tool, we can measure:

* The number of valid leads extracted per week
* Reduction in time spent manually sorting emails
* Percentage of leads imported into CRM from email

---

## 🔗 Future Integrations

To expand the script’s value, future enhancements may include:

* **Microsoft Outlook label-based filters**
* **LinkedIn API** integration to fetch company/individual profiles associated with emails
* **AI tools** for analyzing and scoring leads based on context, sentiment, or urgency
* Export to **Google Sheets** or direct CRM push

---

## 📬 Contact

🔗 GitHub: [https://github.com/siddhirajpantoji/email\_lead\_reader](https://github.com/siddhirajpantoji/email_lead_reader)
📧 Email: [siddhirajpantoji@gmail.com](mailto:siddhirajpantoji@gmail.com)

---

*End of Document*
