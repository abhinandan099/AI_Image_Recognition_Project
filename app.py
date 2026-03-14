import streamlit as st
from detect import detect_objects
import pandas as pd
import datetime
import os

st.set_page_config(page_title="AI Object Detection System", layout="wide")

st.title("AI Image Recognition System")

# -------- Sidebar Navigation --------

page = st.sidebar.selectbox(
    "Navigation",
    ["Object Detection", "Analytics Dashboard"]
)

# -------- OBJECT DETECTION PAGE --------

if page == "Object Detection":

    st.header("Upload Image for AI Detection")

    uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:

        with open("temp.jpg", "wb") as f:
            f.write(uploaded_file.read())

        objects, output_img = detect_objects("temp.jpg")

        st.image(output_img, caption="Detected Objects", use_column_width=True)

        st.subheader("Detected Objects")

        object_counts = {}

        data = []

        for obj, conf in objects:

            st.write(f"{obj} : {conf:.2f}")

            object_counts[obj] = object_counts.get(obj, 0) + 1

            data.append({
                "object": obj,
                "confidence": conf,
                "time": datetime.datetime.now()
            })

        st.subheader("Object Count")

        st.write(object_counts)

        df = pd.DataFrame(data)
