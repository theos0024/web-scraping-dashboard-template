import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob

# ---------------------------
# 1. Settings (Edit per project)
# ---------------------------
PROJECT_TITLE = "📊 Web Scraping Dashboard"
DATA_FILE = "data/cleaned_data.csv"

SEARCH_COLUMNS = ["Title", "Headline", "Name"]
NUMERIC_COLUMNS = ["Price", "Salary", "Population"]
CATEGORICAL_COLUMNS = ["Rating", "Category", "JobType"]
TEXT_COLUMN = "Title"      # For word cloud + sentiment
DATE_COLUMN = "Date"       # For time series

# ---------------------------
# 2. Load Data
# ---------------------------
@st.cache_data
def load_data():
    return pd.read_csv(DATA_FILE)

df = load_data()

# ---------------------------
# 3. Layout
# ---------------------------
st.set_page_config(page_title=PROJECT_TITLE, layout="wide")
st.title(PROJECT_TITLE)
st.write("Interactive dashboard for scraped data.")

# ---------------------------
# 4. Preview
# ---------------------------
st.subheader("📂 Dataset Preview")
st.dataframe(df.head())

# ---------------------------
# 5. Search
# ---------------------------
if SEARCH_COLUMNS:
    st.subheader("🔎 Search")
    search_col = st.selectbox("Column to search:", SEARCH_COLUMNS)
    search_term = st.text_input("Enter keyword:")
    if search_term:
        filtered = df[df[search_col].astype(str).str.contains(search_term, case=False)]
    else:
        filtered = df
else:
    filtered = df

st.write(f"Records: {len(filtered)}")
st.dataframe(filtered)

# ---------------------------
# 6. Numeric Distribution
# ---------------------------
if NUMERIC_COLUMNS:
    st.subheader("💰 Numeric Distribution")
    num_col = st.selectbox("Select numeric column:", NUMERIC_COLUMNS)
    if num_col in filtered.columns:
        fig, ax = plt.subplots()
        filtered[num_col].hist(bins=20, ax=ax)
        ax.set_xlabel(num_col)
        ax.set_ylabel("Count")
        st.pyplot(fig)

# ---------------------------
# 7. Categorical Distribution
# ---------------------------
if CATEGORICAL_COLUMNS:
    st.subheader("⭐ Categorical Distribution")
    cat_col = st.selectbox("Select categorical column:", CATEGORICAL_COLUMNS)
    if cat_col in filtered.columns:
        st.bar_chart(filtered[cat_col].value_counts())

# ---------------------------
# 8. Word Cloud
# ---------------------------
if TEXT_COLUMN and TEXT_COLUMN in filtered.columns:
    st.subheader("☁️ Word Cloud")
    text_data = " ".join(filtered[TEXT_COLUMN].dropna().astype(str).tolist())
    if text_data.strip():
        wc = WordCloud(width=800, height=400, background_color="white").generate(text_data)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wc, interpolation="bilinear")
        ax.axis("off")
        st.pyplot(fig)

# ---------------------------
# 9. Sentiment Analysis
# ---------------------------
if TEXT_COLUMN and TEXT_COLUMN in filtered.columns:
    st.subheader("😊 Sentiment Analysis")
    filtered["Sentiment"] = filtered[TEXT_COLUMN].astype(str).apply(lambda x: TextBlob(x).sentiment.polarity)
    fig, ax = plt.subplots()
    filtered["Sentiment"].hist(bins=20, ax=ax, color="skyblue", edgecolor="black")
    ax.set_title("Sentiment Distribution")
    st.pyplot(fig)

# ---------------------------
# 10. Time Series
# ---------------------------
if DATE_COLUMN and DATE_COLUMN in filtered.columns:
    st.subheader("⏳ Time Series")
    df_time = filtered.copy()
    df_time[DATE_COLUMN] = pd.to_datetime(df_time[DATE_COLUMN], errors="coerce")
    df_time = df_time.dropna(subset=[DATE_COLUMN])
    if not df_time.empty:
        ts_col = st.selectbox("Select numeric column for time series:", NUMERIC_COLUMNS)
        if ts_col in df_time.columns:
            ts_data = df_time.groupby(df_time[DATE_COLUMN].dt.date)[ts_col].mean()
            st.line_chart(ts_data)

# ---------------------------
# 11. Download
# ---------------------------
st.subheader("⬇️ Download Data")
csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "scraped_data.csv", "text/csv")
