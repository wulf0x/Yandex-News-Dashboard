import pandas as pd
import streamlit as st
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

# --- Загрузка данных ---
df = pd.read_csv("reports/news_summary.csv")

# Преобразуем дату, если есть
if 'published' in df.columns:
    df['published'] = pd.to_datetime(df['published'], errors='coerce')
    df.sort_values(by='published', ascending=False, inplace=True)

# --- Заголовок ---
st.title("Дашборд новостей TASS")
st.write("Анализ последних новостей с визуализацией и фильтрацией")

# --- Фильтр по настроению ---
sentiment_options = ["Все", "Позитивные", "Негативные", "Нейтральные"]
choice = st.selectbox("Фильтр по настроению:", sentiment_options)

if choice == "Позитивные":
    df_filtered = df[df['sentiment'] > 0.05]
elif choice == "Негативные":
    df_filtered = df[df['sentiment'] < -0.05]
elif choice == "Нейтральные":
    df_filtered = df[(df['sentiment'] >= -0.05) & (df['sentiment'] <= 0.05)]
else:
    df_filtered = df.copy()

# --- Распределение настроений ---
st.subheader("Распределение настроений")
fig_sentiment = px.histogram(
    df_filtered,
    x="sentiment",
    nbins=20,
    labels={'sentiment': 'Настроение'},
    title="Настроение новостей"
)
st.plotly_chart(fig_sentiment)

# --- Количество слов в заголовках ---
st.subheader("Количество слов в заголовках")
fig_words = px.histogram(
    df_filtered,
    x="word_count",
    nbins=20,
    labels={'word_count': 'Количество слов'},
    title="Длина заголовков"
)
st.plotly_chart(fig_words)

# --- Word Cloud ---
st.subheader("Слова, которые чаще всего встречаются")
all_words = " ".join(df_filtered['clean_title'].dropna().tolist())
all_words = re.sub(r"\b(в|и|на|с|по|что|за|как|для)\b", "", all_words, flags=re.IGNORECASE)  # убрать стоп-слова
wordcloud = WordCloud(width=800, height=400, background_color="white").generate(all_words)

fig_wc, ax = plt.subplots(figsize=(12, 4))
ax.imshow(wordcloud, interpolation='bilinear')
ax.axis('off')
st.pyplot(fig_wc)

# --- Последние новости ---
st.subheader("Последние новости")
# Ссылки кликабельные
def make_clickable(val):
    return f"[{val}]({df_filtered.loc[df_filtered['title']==val, 'link'].values[0]})"

df_filtered_display = df_filtered[['title', 'published', 'sentiment', 'word_count']].copy()
df_filtered_display['title'] = df_filtered_display['title'].apply(make_clickable)
st.write(df_filtered_display.to_html(escape=False), unsafe_allow_html=True)