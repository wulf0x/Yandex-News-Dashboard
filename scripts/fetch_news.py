import feedparser
import json
from datetime import datetime

RSS_URL = "https://tass.com/rss/v2.xml"
DATA_FILE = "data/news.json"

def fetch_news():
    feed = feedparser.parse(RSS_URL)
    news_list = []

    for entry in feed.entries:
        news_item = {
            "title": entry.title,
            "link": entry.link,
            "published": entry.published if "published" in entry else "",
        }
        news_list.append(news_item)

    # Guardar en JSON
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(news_list, f, ensure_ascii=False, indent=4)

    print(f"[INFO] {len(news_list)} новостей сохранено в {DATA_FILE}")

if __name__ == "__main__":
    fetch_news()
