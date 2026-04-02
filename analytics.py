import streamlit as st
import pandas as pd
import os

st.title("Analytics Dashboard")

file_path = "logs/predictions.csv"

if os.path.exists(file_path):
    df = pd.read_csv(file_path)

    st.subheader("Prediction Distribution")
    st.bar_chart(df["prediction"].value_counts())

    st.subheader("Data")
    st.dataframe(df)
else:
    st.warning("No data available")
