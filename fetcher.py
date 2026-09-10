import feedparser
import os
import datetime
from supabase import create_client

# 1. Verify secrets are present
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("Missing SUPABASE_URL or SUPABASE_KEY environment variables!")

print(f"Connecting to Supabase at: {url}")
supabase = create_client(url, key)

# 2. Fetch Google News RSS
RSS_URL = 'https://news.google.com/rss/search?q="Ministry+of+Civil+Aviation"+OR+"Air+India"+OR+"IndiGo"+OR+"SpiceJet"&hl=en-IN&gl=IN&ceid=IN:en'
feed = feedparser.parse(RSS_URL)

print(f"Found {len(feed.entries)} articles from RSS feed.")

# 3. Process and Insert
inserted_count = 0
for entry in feed.entries[:20]:
    title = entry.title
    score = 10
    if any(k in title.lower() for k in ["emergency", "delay", "cancel", "dgca", "probe", "brawl", "strike"]):
        score += 50

    data = {
        "title": title,
        "url": entry.link,
        "source": "Google News",
        "published_at": datetime.datetime.now().isoformat(),
        "score": score
    }

    try:
        response = supabase.table("viral_news").upsert(data, on_conflict="url").execute()
        inserted_count += 1
    except Exception as e:
        print(f"Failed to insert '{title[:30]}...': {e}")

print(f"Successfully processed and inserted {inserted_count} articles.")
