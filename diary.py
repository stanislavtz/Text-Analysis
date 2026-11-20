import streamlit as st
import plotly.express as px
from nltk.sentiment import SentimentIntensityAnalyzer
from pathlib import Path


def define_positivity(text):
    s = sentiment.polarity_scores(text)
    return s.get("pos")


def define_negativity(text):
    s = sentiment.polarity_scores(text)
    return s.get("neg")


sentiment = SentimentIntensityAnalyzer()

filenames = sorted([p.name for p in Path("files").iterdir() if p.is_file()])

dates = [f.strip(".txt") for f in filenames]
positives = []
negatives = []

for filename in filenames:
    with open(f"files/{filename}") as f:
        data = f.read()
        p_value = define_positivity(data)
        positives.append(p_value)

        n_value = define_negativity(data)
        negatives.append(n_value)


st.title("Diary Tone")

st.subheader("Positive")

p_figure = px.line(
    x=dates,
    y=positives,
    labels={"x": "Dates", "y": "Positives"},
)

st.plotly_chart(p_figure)

st.subheader("Negative")

n_figure = px.line(
    x=dates,
    y=negatives,
    labels={"x": "Dates", "y": "Negatives"},
)

st.plotly_chart(n_figure)