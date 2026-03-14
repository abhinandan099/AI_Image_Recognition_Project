import streamlit as st
from detect import detect_objects
from PIL import Image
import os

st.title("AI Object Detection System")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:

    # Save uploaded image
    image = Image.open(uploaded_file)
    image.save("temp.jpg")

    st.image(image, caption="Uploaded Image", use_column_width=True)

    st.write("Detecting objects...")

    objects = detect_objects("temp.jpg")

    st.subheader("Detected Objects")

    if len(objects) == 0:
        st.write("No objects detected")
    else:
        for obj in objects:
            st.write(f"{obj[0]} : {round(obj[1]*100,2)}%")
