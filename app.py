import streamlit as st
from detect import detect_objects
from predict import predict_image
from logger import log_prediction
import pandas as pd
import os
import time

st.set_page_config(page_title="AI Image Recognition", layout="wide")

st.title("AI Image Recognition System")

page = st.sidebar.selectbox("Navigation", ["Detection", "Analytics"])

if page == "Detection":

    uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

    if uploaded_file is not None:

        file_bytes = uploaded_file.read()

        if len(file_bytes) == 0:
            st.error("Uploaded file is empty ❌")
        else:
            with open("temp.jpg", "wb") as f:
                f.write(file_bytes)

            time.sleep(0.5)  # FIX timing issue

            try:
                objects, output_img = detect_objects("temp.jpg")

                st.image(output_img, caption="Detected Objects")

                st.subheader("Objects Found")
                object_names = [obj for obj, _ in objects]

                for obj, conf in objects:
                    st.write(f"{obj} : {conf:.2f}")

                food_items = ["banana","apple","orange","pizza","cake"]

                if any(obj in food_items for obj in object_names):
                    label, confidence = predict_image("temp.jpg")

                    st.subheader("Food Freshness")
                    st.success(label)
                    st.write(f"Confidence: {confidence:.2f}")

                    log_prediction("temp.jpg", label, confidence)
                else:
                    st.info("No food detected → skipping freshness")

            except Exception as e:
                st.error(f"❌ Error: {e}")

elif page == "Analytics":

    file_path = "logs/predictions.csv"

    if os.path.exists(file_path):
        df = pd.read_csv(file_path)

        st.bar_chart(df["prediction"].value_counts())
        st.dataframe(df)
    else:
        st.warning("No data yet")