import json
import sys
import os
#Adding parent directory as to the list of paths Python searches for modules to import private
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import asyncio
from datetime import date, datetime
import time
import private
import feedparser

def letturafeedrss():
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
        print(",\n".join(titles))


    titles2 = [(x["title"]) for x in feed2.entries]

    with open("titles2.json" , "w") as f:
        json.dump(titles2, fp=f, indent=4)
        print(",\n".join(titles2))

def main():
    while True:
        print("-----Esecuzione ogni 10 secondi-----")
        letturafeedrss()
        print("-----Prossima esecuzione tra 10 secondi-----")
        time.sleep(10)  # tempo in secondi

# Chiamata ai programmi
if __name__ == "__main__":
    main()