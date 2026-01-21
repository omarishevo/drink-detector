import streamlit as st
from PIL import Image

st.set_page_config(page_title="🥤 Drink Detector", layout="centered")
st.title("🥤 Simple Drink Label Detector")
st.write("This version does not use TensorFlow or PyTorch. It uses a simple label mapping.")

# -------------------------------
# Load Labels
# -------------------------------
labels_file = "labels.txt"
with open(labels_file, "r") as f:
    drink_labels = [line.strip() for line in f.readlines()]

# -------------------------------
# Upload Image
# -------------------------------
uploaded_file = st.file_uploader("Upload Drink Image", type=["jpg", "jpeg", "png"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # -------------------------------
    # Simple detection (filename match)
    # -------------------------------
    detected_label = "Unknown"

    # Check if any label is in the filename
    filename = uploaded_file.name.lower()
    for label in drink_labels:
        if label.lower().replace(" ", "") in filename:
            detected_label = label
            break

    st.write(f"### 🏷️ Detected Drink Label: **{detected_label}**")
