import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("AI Detection Analytics Dashboard")

df = pd.read_csv("predictions.csv")

counts = df["object"].value_counts()

st.bar_chart(counts)

st.write(df)
