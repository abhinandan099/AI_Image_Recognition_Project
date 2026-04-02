import streamlit as st
from detect import detect_objects
import os

st.set_page_config(page_title="AI Image Recognition", layout="centered")

st.title("🧠 AI Image Recognition App")
st.write("Upload an image and detect objects like car, bike, person, etc.")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save uploaded file
    with open("temp.jpg", "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image("temp.jpg", caption="Uploaded Image", use_column_width=True)

    st.write("🔍 Detecting objects...")

    # Run detection
    objects, output_img = detect_objects("temp.jpg")

    if objects:
        st.subheader("Detected Objects:")
        for obj in objects:
            st.write(f"✅ {obj}")
    else:
        st.warning("No objects detected")

    st.image(output_img, caption="Detection Result", use_column_width=True)

    # Clean up temp file
    if os.path.exists("temp.jpg"):
        os.remove("temp.jpg")