import streamlit as st
import pandas as pd
import os

st.title("AI Detection Analytics Dashboard")

if os.path.exists("predictions.csv"):
    df = pd.read_csv("predictions.csv")
    counts = df["object"].value_counts()
    st.bar_chart(counts)
    st.write(df)
else:
    st.warning("No data found. Please run a detection first to generate predictions.csv.")