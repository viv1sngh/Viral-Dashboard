import feedparser
import os
import datetime
from supabase import create_client, Client

# 1. Connect to Database
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# 2. Define the Aviation Search Query
RSS_URL = 'https://news.google.com/rss/search?q="Ministry+of+Civil+Aviation"+OR+"DGCA"+OR+"AAI"+OR+"Airports+Authority+of+India"+OR+"Air+India"+OR+"IndiGo"+OR+"SpiceJet"+OR+"Air+India+Express"+OR+"Alliance+Air"+OR+"Akasa+Air"&hl=en-IN&gl=IN&ceid=IN:en'

feed = feedparser.parse(RSS_URL)

# 3. Process and Score Articles
for entry in feed.entries[:30]:
    title = entry.title
    # Base score of 10. Boost score if critical keywords are present.
    score = 10 
    if any(keyword in title.lower() for keyword in ["emergency", "delay", "cancel", "dgca", "probe", "brawl", "lost", "baggage", "missing", "delayed", "damaged", "received", "luggage, "issue", "Check-in", "Boarding", "gate", "change", "overbooking", "Flight", "Delays", "Cancellations", "cancelled", "diverted", "missed", "connection", "Ticketing", "Fare", "Refund", "fare", "Crew", "Behaviour", "Rude", "wheelchair", "assistance", "PRM", "issue", "Airsewa", "Passenger", "Complaint", "Postponed", "airport", "food", "broken", "BCAS", "Domestic", "International", "Ticket", "PNR", "conveyor", "belt", "waiting", "Ground", "Security", "Breach", "seat", "travel", "traveling", "travelling", "travelled", "Aviation", "meltdown", "scheduled", "crisis", "Pending", "Failed, "Compensation", "claim", "chaos", "AC", "working", "Boarding", "sleeping", "Portal", "waiting", "Shouting", "Problem", "Helpless", "Assistance", "Queue", "Situation", "Pathetic", "Money", "Pilot", "Immigration", "Customs", "smuggling", "illegal", "unauthorized", "fog", "medical"]):
        score += 50
    
    data = {
        "title": title,
        "url": entry.link,
        "source": "Google News",
        "published_at": datetime.datetime.now().isoformat(),
        "score": score
    }
    
    # 4. Insert into database (ignores if URL already exists)
    try:
        supabase.table("viral_news").upsert(data, on_conflict="url").execute()
    except Exception as e:
        pass # Silently skip duplicates