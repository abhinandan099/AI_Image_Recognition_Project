import streamlit as st
from detect import detect_objects
from PIL import Image

st.title("AI Object Detection System")

st.write("Upload an image and the AI will detect objects.")

uploaded_file = st.file_uploader("Upload Image", type=["jpg","png","jpeg"])

if uploaded_file is not None:

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
