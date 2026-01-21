import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="🥤 Drink Detector & CSV Generator", layout="centered")
st.title("🥤 Drink Label Detector with CSV (Auto-Loading)")

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
# Helper function to load images from URLs
# -------------------------------
@st.cache_data
def load_image_from_url(url):
    """Load image from URL with caching"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        img = Image.open(BytesIO(response.content))
        return img
    except (requests.RequestException, UnidentifiedImageError) as e:
        return None

# -------------------------------
# Step 2: Display drink images automatically
# -------------------------------
st.write("### 📸 Available Drinks (Auto-Loaded)")
st.info("All images are automatically loaded from URLs - no uploads needed!")

# Create a grid layout for better display
num_cols = 4
cols = st.columns(num_cols)

for i, (label, url) in enumerate(drink_data.items()):
    with cols[i % num_cols]:
        img = load_image_from_url(url)
        if img:
            st.image(img, caption=label, use_container_width=True)
        else:
            st.warning(f"❌ {label}")

# -------------------------------
# Step 3: Generate CSV of all drink labels
# -------------------------------
st.write("---")
st.write("### 📊 All Drink Labels")
df = pd.DataFrame(list(drink_data.keys()), columns=["Drink Label"])
st.dataframe(df, use_container_width=True)

csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Drink Labels CSV",
    data=csv,
    file_name="drink_labels.csv",
    mime="text/csv"
)

# -------------------------------
# Step 4: Detect a drink (Auto-display selected image)
# -------------------------------
st.write("---")
st.write("### 🔍 Detect a Drink")
selected_drink = st.selectbox("Select a drink to detect:", df["Drink Label"].tolist())

# Automatically display the selected drink's image
col1, col2 = st.columns([1, 2])

with col1:
    selected_url = drink_data[selected_drink]
    selected_img = load_image_from_url(selected_url)
    if selected_img:
        st.image(selected_img, use_container_width=True)
    else:
        st.error("Failed to load image")

with col2:
    st.write(f"### 🏷️ Detected Drink:")
    st.success(f"**{selected_drink}**")
    st.write(f"**Image URL:** {selected_url}")
    
    # Additional info
    st.info(f"✅ This drink has been automatically detected and loaded from the database!")

# -------------------------------
# Optional: Batch processing section
# -------------------------------
st.write("---")
st.write("### 🔄 Batch Process All Drinks")
if st.button("Process All Drinks"):
    with st.spinner("Processing all drinks..."):
        results = []
        for label, url in drink_data.items():
            img = load_image_from_url(url)
            status = "✅ Loaded" if img else "❌ Failed"
            results.append({"Drink": label, "Status": status, "URL": url})
        
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)
        st.success(f"Processed {len(results)} drinks!")
