import json
import pandas as pd
from textblob import TextBlob
import re

DATA_FILE = "data/news.json"
OUTPUT_FILE = "reports/news_summary.csv"

def clean_text(text):
    return re.sub(r"[^а-яА-Яa-zA-Z0-9\s]", "", text)

def analyze_news():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        news = json.load(f)

    df = pd.DataFrame(news)
    df['clean_title'] = df['title'].apply(clean_text)
    df['word_count'] = df['clean_title'].apply(lambda x: len(x.split()))
    df['sentiment'] = df['clean_title'].apply(lambda x: TextBlob(x).sentiment.polarity)

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"[INFO] Анализ сохранен в {OUTPUT_FILE}")

if __name__ == "__main__":
    analyze_news()
