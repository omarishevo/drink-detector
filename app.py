import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="🥤 Drink Detector & CSV Generator", layout="centered")
st.title("🥤 Drink Label Detector with CSV (Stable Version)")

# -------------------------------
# Step 1: Define 20 stable drink image URLs (Imgur)
# -------------------------------
drink_data = {
    "Coca-Cola": "https://i.imgur.com/u6jhjJW.jpg",
    "Pepsi": "https://i.imgur.com/7Z7FjQv.jpg",
    "Red Bull": "https://i.imgur.com/2j1Nsdn.jpg",
    "Sprite": "https://i.imgur.com/6fOeJ4K.jpg",
    "Fanta": "https://i.imgur.com/g3cqTjB.jpg",
    "Monster Energy": "https://i.imgur.com/q8b3bQX.jpg",
    "Minute Maid": "https://i.imgur.com/Df3tEmk.jpg",
    "Dasani": "https://i.imgur.com/R2krkVr.jpg",
    "Lipton Ice Tea": "https://i.imgur.com/7kIYw0v.jpg",
    "Milo": "https://i.imgur.com/NnJc5gK.jpg",
    "7UP": "https://i.imgur.com/3xQ9s5x.jpg",
    "Lucozade": "https://i.imgur.com/5cUoFkg.jpg",
    "Tropicana": "https://i.imgur.com/1D8ZxjM.jpg",
    "Heineken": "https://i.imgur.com/3bI7tGb.jpg",
    "Guinness": "https://i.imgur.com/8O1r2Qo.jpg",
    "Baileys": "https://i.imgur.com/nR3e2Yv.jpg",
    "Aquafina": "https://i.imgur.com/w8uZ1vN.jpg",
    "Schweppes": "https://i.imgur.com/Gh5XQ3K.jpg",
    "Nestle Pure Life": "https://i.imgur.com/VGQf6Wz.jpg",
    "Lipton Yellow Label Tea": "https://i.imgur.com/0mSeD5K.jpg"
}

# -------------------------------
# Step 2: Display drink images
# -------------------------------
st.write("### Available Drinks")
cols = st.columns(len(drink_data)//2)  # display in 2 rows
for i, (label, url) in enumerate(drink_data.items()):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        cols[i % len(cols)].image(img, caption=label, use_column_width=True)
    except (requests.RequestException, UnidentifiedImageError) as e:
        cols[i % len(cols)].write(f"Failed to load {label}")

# -------------------------------
# Step 3: Generate CSV of all drink labels
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
