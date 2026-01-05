
import feedparser
import os
from datetime import datetime
from collections import defaultdict

BASE_DIR = "categories"
STATUS_FILE = "STATUS.md"
MAX_POSTS = 15
TODAY = datetime.utcnow().strftime("%d %B %Y")

RSS_SOURCES = {
    "HackerOne": "https://www.hackerone.com/blog.rss",
    "PortSwigger": "https://portswigger.net/research/rss",
    "Bugcrowd": "https://www.bugcrowd.com/blog/feed/",
}

MEDIUM_TAGS = {
    "xss": ["xss"],
    "sqli": ["sql-injection"],
    "ssrf": ["ssrf"],
    "idor": ["idor"],
    "account-takeover": ["account-takeover"],
    "broken-access-control": ["access-control"],
    "oauth": ["oauth"],
    "2fa": ["2fa"],
    "api-security": ["api-security"],
    "cloud-security": ["cloud-security"],
    "business-logic": ["business-logic"],
    "misconfiguration": ["misconfiguration"],
    "subdomain-takeover": ["subdomain-takeover"],
    "malware": ["malware"],
    "recon": ["recon", "bug-bounty"],
}

CATEGORY_KEYWORDS = {
    "broken-access-control": ["broken access", "access control"],
    "account-takeover": ["account takeover", "ato"],
    "idor": ["idor"],
    "privilege-escalation": ["privilege escalation"],
    "authentication-bypass": ["authentication bypass"],
    "authorization-bypass": ["authorization bypass"],
    "2fa": ["2fa", "two-factor"],
    "otp": ["otp"],
    "password-reset": ["password reset"],
    "oauth": ["oauth"],
    "sso": ["sso"],
    "jwt": ["jwt"],
    "xss": ["xss"],
    "sqli": ["sql injection", "sqli"],
    "command-injection": ["command injection"],
    "rce": ["remote code", "rce"],
    "ssti": ["ssti"],
    "xxe": ["xxe"],
    "deserialization": ["deserialization"],
    "ssrf": ["ssrf"],
    "csrf": ["csrf"],
    "open-redirect": ["open redirect"],
    "host-header-injection": ["host header"],
    "http-smuggling": ["http smuggling"],
    "business-logic": ["business logic"],
    "race-condition": ["race condition"],
    "price-manipulation": ["price manipulation"],
    "workflow-bypass": ["workflow bypass"],
    "api-security": ["api"],
    "graphql": ["graphql"],
    "mass-assignment": ["mass assignment"],
    "rate-limiting": ["rate limit"],
    "cloud-security": ["aws", "azure", "gcp", "cloud"],
    "misconfiguration": ["misconfiguration"],
    "secrets-exposure": ["api key", "secret"],
    "subdomain-takeover": ["subdomain takeover"],
    "malware": ["malware"],
    "supply-chain": ["supply chain"],
    "browser-security": ["browser"],
    "mobile-security": ["android", "ios"],
    "recon": ["recon"],
    "information-disclosure": ["information disclosure"],
    "fingerprinting": ["fingerprint"],
}

stats_daily = defaultdict(int)
stats_category = defaultdict(int)
stats_source = defaultdict(int)

def date_fmt(d):
    return datetime(*d[:6]).strftime("%d %B %Y")

def existing_links(path):
    if not os.path.exists(path):
        return set()
    with open(path, encoding="utf-8") as f:
        return set(l for l in f if "http" in l)

def write_entry(category, date, line, source):
    path = f"{BASE_DIR}/{category}.md"
    os.makedirs(BASE_DIR, exist_ok=True)

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# {category.replace('-', ' ').title()}\n\n")

    if line in existing_links(path):
        return False

    with open(path, "r+", encoding="utf-8") as f:
        old = f.read()
        f.seek(0)
        f.write(f"## 📅 {date}\n\n{line}\n" + old)

    stats_daily[date] += 1
    stats_category[category] += 1
    stats_source[source] += 1
    return True

# -------- MEDIUM --------
for cat, tags in MEDIUM_TAGS.items():
    for tag in tags:
        feed = feedparser.parse(f"https://medium.com/feed/tag/{tag}")
        for e in feed.entries[:MAX_POSTS]:
            write_entry(
                cat,
                date_fmt(e.published_parsed),
                f"- **[{e.title}]({e.link})** _(Medium)_",
                "Medium"
            )

# -------- OTHER BLOGS --------
for source, url in RSS_SOURCES.items():
    feed = feedparser.parse(url)
    for e in feed.entries[:MAX_POSTS]:
        title = e.title.lower()
        date = date_fmt(e.published_parsed)
        for cat, keys in CATEGORY_KEYWORDS.items():
            if any(k in title for k in keys):
                write_entry(
                    cat,
                    date,
                    f"- **[{e.title}]({e.link})** _({source})_",
                    source
                )

# -------- STATUS PAGE --------
with open(STATUS_FILE, "w", encoding="utf-8") as f:
    f.write("# 📊 Security Writeups Status\n\n")
    f.write(f"**Last Updated:** {datetime.utcnow().strftime('%d %B %Y %H:%M UTC')}\n\n")

    f.write("## 📅 Today\n")
    f.write(f"- New writeups today: **{stats_daily.get(TODAY, 0)}**\n\n")

    f.write("## 📈 Activity (Last 7 Days)\n")
    for d in sorted(stats_daily.keys(), reverse=True)[:7]:
        f.write(f"- {d}: **{stats_daily[d]}**\n")

    f.write("\n## 📂 Writeups by Category\n")
    for c, count in sorted(stats_category.items(), key=lambda x: x[1], reverse=True):
        f.write(f"- {c}: **{count}**\n")

    f.write("\n## 🌐 Writeups by Source\n")
    for s, count in stats_source.items():
        f.write(f"- {s}: **{count}**\n")
