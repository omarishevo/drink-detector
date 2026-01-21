import streamlit as st
from PIL import Image
import requests
from io import BytesIO

st.set_page_config(page_title="🥤 Auto Drink Detector", layout="centered")
st.title("🥤 Drink Detector Demo (No Upload Needed)")

# -------------------------------
# Drink images URLs (example)
# -------------------------------
drink_data = {
    "Coca-Cola": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_can.jpg",
    "Pepsi": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Pepsi_can.jpg",
    "Red Bull": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Red_Bull_can.jpg",
    "Sprite": "https://upload.wikimedia.org/wikipedia/commons/3/36/Sprite_can.jpg",
    "Fanta": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Fanta_can.jpg"
}

# -------------------------------
# Display drink images
# -------------------------------
st.write("### Available Drinks")
cols = st.columns(len(drink_data))
for col, (label, url) in zip(cols, drink_data.items()):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    col.image(img, caption=label, use_column_width=True)

# -------------------------------
# User selects a drink to detect
# -------------------------------
selected_drink = st.selectbox("Select a drink to detect:", list(drink_data.keys()))

st.write(f"### 🏷️ Detected Drink: **{selected_drink}**")
