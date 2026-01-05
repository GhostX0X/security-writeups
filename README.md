# security-writeups

## 🤖 Automated Security Writeups Tracker

This repository automatically tracks and categorizes security writeups from:

- Medium (security & bug bounty blogs)
- HackerOne disclosures
- PortSwigger research
- Bugcrowd blogs

### 🔄 How it works
- A GitHub Actions workflow runs every **6 hours**
- Fetches latest security writeups via RSS feeds
- Automatically categorizes them (XSS, SSRF, IDOR, etc.)
- Updates markdown files inside the `categories/` directory
- Updates `STATUS.md` with run statistics

### ⏱ Schedule
- Runs automatically every **6 hours**
- Can also be triggered manually from the **Actions** tab

### 📁 Repository Structure
