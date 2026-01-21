import streamlit as st
import numpy as np
from PIL import Image
import tensorflow as tf

# -------------------------------
# App Config
# -------------------------------
st.set_page_config(page_title="🥤 Drink Detector", layout="centered")
st.title("🥤 Drink Label Detection System")
st.write("Upload a drink image to identify its label or brand.")

# -------------------------------
# Load Model
# -------------------------------
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("drink_detector.h5")

model = load_model()

# -------------------------------
# Load Labels
# -------------------------------
with open("labels.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# -------------------------------
# Preprocess Image
# -------------------------------
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    image = np.expand_dims(image, axis=0)
    return image

# -------------------------------
# Upload Image
# -------------------------------
uploaded_file = st.file_uploader("Upload Drink Image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Detect Drink Label"):
        with st.spinner("Detecting..."):
            img_array = preprocess_image(image)
            predictions = model.predict(img_array)
            confidence = np.max(predictions)
            predicted_class = class_names[np.argmax(predictions)]

        st.success("Detection Complete!")
        st.write(f"### 🏷️ Predicted Drink: **{predicted_class}**")
        st.write(f"### 📊 Confidence: **{confidence*100:.2f}%**")
