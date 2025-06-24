# 💼 Pitch Deck: Email Lead Extractor

---

## Slide 1: 🚀 Idea Overview

**Email Lead Extractor**
An automation tool to convert unread emails into qualified leads from **Gmail** or **Outlook** and extract contact info into structured CSVs.

---

## Slide 2: 😩 The Problem

Manual inbox scanning leads to:

* Missed opportunities
* Inefficient follow-ups
* Poor CRM data quality
* No integration with lead systems or analysis

---

## Slide 3: 💡 Our Solution

A cross-provider script that:

* Connects securely to Gmail via IMAP and Outlook via Microsoft Graph API
* Detects lead-related emails based on smart keyword filtering
* Extracts contact info: emails and phone numbers
* Exports leads to a timestamped CSV inside `/output/`

---

## Slide 4: 🔧 Key Features

* Gmail IMAP integration
* Outlook Microsoft Graph API integration
* Keyword-based lead filtering (subject/body)
* Contact info extraction via regex
* Config-driven using `config.csv`
* `MARK_AS_READ` toggle
* Output saved to timestamped CSV files

---

## Slide 5: ✅ MVP

* Read 20 unread emails from Gmail or Outlook
* Identify leads based on keywords
* Extract email addresses and phone numbers
* Save results to `output/leads_<timestamp>.csv`
* Mark as read if enabled in config

---

## Slide 6: 💸 Business Model

* Open-source CLI tool (free)
* Paid upgrade with GUI and CRM integrations
* Enterprise package with Slack alerts, auto-replies, and AI analysis

---

## Slide 7: 🤞 Market Landscape

| Tool          | Pros                        | Cons                     |
| ------------- | --------------------------- | ------------------------ |
| Zapier        | Easy automation             | Expensive at scale       |
| Mailparser.io | Powerful parsing, templates | Paid-only, setup-heavy   |
| Our Solution  | Free, simple, configurable  | CLI only (UI in roadmap) |

---

## Slide 8: 📊 Success Metrics

* Valid leads extracted weekly
* % of emails converted into contacts
* Time saved vs. manual sorting
* GitHub usage & stars
* User adoption & feedback

---

## Slide 9: 🔗 Future Integrations

* Microsoft Outlook label-based filtering
* **LinkedIn API** for lead enrichment
* **AI** scoring of leads (sentiment, priority)
* Google Sheets or CRM sync

---

## Slide 10: 📬 Get in Touch

🔗 GitHub: [github.com/siddhirajpantoji/email\_lead\_reader](https://github.com/siddhirajpantoji/email_lead_reader)
📧 Email: [siddhirajpantoji@gmail.com](mailto:siddhirajpantoji@gmail.com)

---

*Thank you!*
