import streamlit as st
import pandas as pd

st.set_page_config(page_title="🥤 Drink Label CSV & Detector", layout="centered")
st.title("🥤 Drink Labels Collector & Detector")

# -------------------------------
# Step 1: Define drink labels
# -------------------------------
drink_labels = [
    "Coca-Cola", "Pepsi", "Red Bull", "Sprite", "Fanta",
    "Monster Energy", "Minute Maid", "Dasani", "Lipton Ice Tea",
    "Milo", "Nestle Pure Life", "Aquafina", "Schweppes",
    "7UP", "Lucozade", "Tropicana", "Heineken", "Guinness", "Baileys"
]

# Create a DataFrame
df = pd.DataFrame(drink_labels, columns=["Drink Label"])

# -------------------------------
# Step 2: Display CSV and download
# -------------------------------
st.write("### All Drink Labels")
st.dataframe(df)

# Generate CSV for download
csv = df.to_csv(index=False)
st.download_button(
    label="📥 Download Drink Labels CSV",
    data=csv,
    file_name="drink_labels.csv",
    mime="text/csv"
)

# -------------------------------
# Step 3: Detect a drink
# -------------------------------
st.write("### Detect a Drink Label")
selected_drink = st.selectbox("Select a drink to detect:", df["Drink Label"].tolist())

st.write(f"### 🏷️ Detected Drink: **{selected_drink}**")
