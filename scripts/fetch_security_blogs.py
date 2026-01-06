import feedparser
import os
from datetime import datetime
from collections import defaultdict

BASE_DIR = "categories"
STATUS_FILE = "STATUS.md"
MAX_POSTS = 10

RSS_SOURCES = {
    # Platforms
    "HackerOne Hacktivity": "https://hackerone.com/hacktivity.rss",
    "PortSwigger Research": "https://portswigger.net/research/rss",
    "Bugcrowd Blog": "https://www.bugcrowd.com/blog/feed/",

    # Medium (VERY IMPORTANT)
    "Medium Security": "https://medium.com/feed/tag/security",
    "Medium Bug Bounty": "https://medium.com/feed/tag/bug-bounty",
    "Medium Pentesting": "https://medium.com/feed/tag/pentesting",
}

KEYWORDS = {
    "xss": ["xss"],
    "sqli": ["sql injection", "sqli"],
    "ssrf": ["ssrf"],
    "account-takeover": ["account takeover", "ato"],
    "broken-access-control": ["access control"],
    "idor": ["idor"],
    "oauth": ["oauth"],
    "csrf": ["csrf"],
    "rce": ["rce"],
    "recon": ["recon"],
}

def fmt_date(d):
    return datetime(*d[:6]).strftime("%d %B %Y")

def append(category, date, line):
    os.makedirs(BASE_DIR, exist_ok=True)
    path = f"{BASE_DIR}/{category}.md"

    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(f"# {category.replace('-', ' ').title()}\n\n")

    with open(path, "r+", encoding="utf-8") as f:
        content = f.read()
        if line in content:
            return
        f.seek(0)
        f.write(f"## 📅 {date}\n\n{line}\n" + content)

stats = defaultdict(int)

for source, url in RSS_SOURCES.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:MAX_POSTS]:
        title = entry.title.lower()
        date = fmt_date(entry.published_parsed)

        for cat, words in KEYWORDS.items():
            if any(w in title for w in words):
                append(
                    cat,
                    date,
                    f"- **[{entry.title}]({entry.link})** _({source})_"
                )
                stats[cat] += 1

with open(STATUS_FILE, "w") as f:
    f.write("# 📊 Status\n\n")
    f.write(f"Last updated: {datetime.utcnow()} UTC\n\n")
    for k, v in stats.items():
        f.write(f"- {k}: {v}\n")

