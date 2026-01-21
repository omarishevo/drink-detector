import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO

st.set_page_config(page_title="🥤 Auto Drink Detector", layout="centered")
st.title("🥤 Drink Detector Demo (No Upload Needed)")

# Drink image URLs (direct image links)
drink_data = {
    "Coca-Cola": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_can.jpg",
    "Pepsi": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Pepsi_can.jpg",
    "Red Bull": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Red_Bull_can.jpg",
    "Sprite": "https://upload.wikimedia.org/wikipedia/commons/3/36/Sprite_can.jpg",
    "Fanta": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Fanta_can.jpg"
}

st.write("### Available Drinks")
cols = st.columns(len(drink_data))

for col, (label, url) in zip(cols, drink_data.items()):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # check for HTTP errors
        img = Image.open(BytesIO(response.content))
        col.image(img, caption=label, use_column_width=True)
    except (requests.RequestException, UnidentifiedImageError) as e:
        col.write(f"Failed to load {label}")
        print(f"Error loading {label}: {e}")

# User selects a drink to detect
selected_drink = st.selectbox("Select a drink to detect:", list(drink_data.keys()))
st.write(f"### 🏷️ Detected Drink: **{selected_drink}**")
