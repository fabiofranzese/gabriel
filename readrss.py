import feedparser
import json

rss_url = "https://sec.cloudapps.cisco.com/security/center/eventResponses_20.xml"
rss_url2 = "https://feeds.feedburner.com/TheHackersNews"

feed = feedparser.parse(rss_url)
feed2 = feedparser.parse(rss_url2)

items = feed.entries
items2 = feed.entries

#APRE TUTTI GLI ITEMS NEL JSON 
#with open("items.json" , "w") as f:
#    json.dump(items, fp=f, indent=4)

#APRE SOLO I TITOLI NEL FILE JSON
titles = [(x["title"]) for x in feed.entries]

with open("titles.json" , "w") as f:
    json.dump(titles, fp=f, indent=4)

titles2 = [(x["title"]) for x in feed2.entries]

with open("titles2.json" , "w") as f:
    json.dump(titles2, fp=f, indent=4)