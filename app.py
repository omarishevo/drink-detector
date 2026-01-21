import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="🥤 Drink Detector & CSV Generator", layout="centered")
st.title("🥤 Drink Label Detector with CSV")

# -------------------------------
# Step 1: Define drinks and image URLs
# -------------------------------
drink_data = {
    "Coca-Cola": "https://upload.wikimedia.org/wikipedia/commons/c/ce/Coca-Cola_can.jpg",
    "Pepsi": "https://upload.wikimedia.org/wikipedia/commons/5/5d/Pepsi_can.jpg",
    "Red Bull": "https://upload.wikimedia.org/wikipedia/commons/4/4e/Red_Bull_can.jpg",
    "Sprite": "https://upload.wikimedia.org/wikipedia/commons/3/36/Sprite_can.jpg",
    "Fanta": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Fanta_can.jpg",
    "Monster Energy": "https://upload.wikimedia.org/wikipedia/commons/2/25/Monster_Energy_can.jpg",
    "Minute Maid": "https://upload.wikimedia.org/wikipedia/commons/f/f6/Minute_Maid_Orange.jpg",
    "Dasani": "https://upload.wikimedia.org/wikipedia/commons/2/2c/Dasani_bottle.jpg",
    "Lipton Ice Tea": "https://upload.wikimedia.org/wikipedia/commons/4/44/Lipton_Ice_Tea.jpg",
    "Milo": "https://upload.wikimedia.org/wikipedia/commons/b/b7/Milo_can.jpg"
}

# -------------------------------
# Step 2: Display drink images
# -------------------------------
st.write("### Available Drinks")
cols = st.columns(len(drink_data))
for col, (label, url) in zip(cols, drink_data.items()):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        col.image(img, caption=label, use_column_width=True)
    except (requests.RequestException, UnidentifiedImageError) as e:
        col.write(f"Failed to load {label}")

# -------------------------------
# Step 3: Generate CSV
# -------------------------------
df = pd.DataFrame(list(drink_data.keys()), columns=["Drink Label"])
st.write("### All Drink Labels")
st.dataframe(df)

csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Drink Labels CSV",
    data=csv,
    file_name="drink_labels.csv",
    mime="text/csv"
)

# -------------------------------
# Step 4: Detect a drink
# -------------------------------
st.write("### Detect a Drink")
selected_drink = st.selectbox("Select a drink to detect:", df["Drink Label"].tolist())
st.write(f"### 🏷️ Detected Drink: **{selected_drink}**")
