import streamlit as st
from PIL import Image
import pandas as pd
import os

# -------------------------------
# CONFIG
# -------------------------------
st.set_page_config(page_title="🥤 Drink Label Detector", layout="wide")
st.title("🥤 Drink Label Detector & CSV Generator")

# -------------------------------
# IMAGE DIRECTORY
# -------------------------------
IMAGE_DIR = "images"

# -------------------------------
# LOAD DATABASE
# -------------------------------
@st.cache_data
def load_drink_database():
    data = {
        "Category": [
            "Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic",
            "Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic",
            "Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Alcoholic","Alcoholic",
            "Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic"
        ],
        "Type": [
            "Soft Drink","Soft Drink","Energy Drink","Soft Drink","Soft Drink",
            "Energy Drink","Juice","Water","Tea","Coffee",
            "Soft Drink","Energy Drink","Juice","Beer","Beer",
            "Liqueur","Water","Soft Drink","Water"
        ],
        "Subtype": [
            "Cola","Cola","Regular","Lemon-Lime","Orange Soda",
            "Regular","Orange Juice","Mineral Water","Iced Tea","Chocolate Drink",
            "Lemon-Lime","Sports Drink","Orange Juice","Lager","Stout",
            "Cream Liqueur","Purified Water","Ginger Ale","Spring Water"
        ],
        "Brand": [
            "Coca-Cola","Pepsi","Red Bull","Sprite","Fanta",
            "Monster","Minute Maid","Dasani","Lipton","Milo",
            "7UP","Lucozade","Tropicana","Heineken","Guinness",
            "Baileys","Aquafina","Schweppes","Nestle"
        ],
        "Label": [
            "Carbonated Soft Drink","Cola Carbonated Soft Drink","Energy Drink",
            "Lemon-Lime Soda","Orange Soda","Energy Drink",
            "Premium Orange Juice","Purified Water","Iced Tea","Chocolate Malt Drink",
            "Lemon Lime Soda","Energy Drink","100% Pure Orange Juice",
            "Premium Lager Beer","Draught Stout",
            "Irish Cream","Purified Drinking Water","Ginger Ale",
            "Pure Life Water"
        ],
        "Image_File": [
            "cocacola.jpg","pepsi.jpg","redbull.jpg","sprite.jpg","fanta.jpg",
            "monster.jpg","minute_maid.jpg","dasani.jpg","lipton.jpg","milo.jpg",
            "7UP.jpg","lucozade.jpg","tropicana.jpg","heineken.jpg","guinness.jpg",
            "baileys.jpg","aquafina.jpg","schweppes.jpg","nestle.jpg"
        ]
    }

    df = pd.DataFrame(data)
    # Add full path
    df["Image_Path"] = df["Image_File"].apply(lambda x: os.path.join(IMAGE_DIR, x))
    # Keep only rows with existing images
    df = df[df["Image_Path"].apply(os.path.exists)].reset_index(drop=True)
    return df

drinks_df = load_drink_database()

# -------------------------------
# LOAD IMAGE
# -------------------------------
@st.cache_data
def load_image(path):
    if os.path.exists(path):
        return Image.open(path).convert("RGB")
    return None

# -------------------------------
# SIDEBAR
# -------------------------------
with st.sidebar:
    st.header("📊 Database Stats")
    st.metric("Total Drinks", len(drinks_df))
    st.metric("Categories", drinks_df["Category"].nunique())
    st.metric("Brands", drinks_df["Brand"].nunique())
    st.download_button(
        "📥 Download Full Database CSV",
        drinks_df.to_csv(index=False),
        "drink_labels_database.csv",
        "text/csv"
    )

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3 = st.tabs(["🔍 Detect Drink", "📸 Gallery", "📊 Database"])

# TAB 1: Detect Drink
with tab1:
    brand = st.selectbox("Select Brand", drinks_df["Brand"].unique())
    drink = drinks_df[drinks_df["Brand"] == brand].iloc[0]

    col1, col2 = st.columns([1, 2])
    with col1:
        img = load_image(drink["Image_Path"])
        if img:
            st.image(img, use_container_width=True)
        else:
            st.warning("Image not found")
    with col2:
        st.success(f"**Brand:** {drink['Brand']}")
        st.write(f"**Label:** {drink['Label']}")
        st.write(f"**Category:** {drink['Category']}")
        st.write(f"**Type:** {drink['Type']}")
        st.write(f"**Subtype:** {drink['Subtype']}")

# TAB 2: Gallery
with tab2:
    cols = st.columns(4)
    for i, row in drinks_df.iterrows():
        with cols[i % 4]:
            img = load_image(row["Image_Path"])
            if img:
                st.image(img, caption=row["Brand"], use_container_width=True)

# TAB 3: Database
with tab3:
    st.dataframe(drinks_df, use_container_width=True)

# -------------------------------
# FOOTER
# -------------------------------
st.write("---")
st.caption("🥤 Drink Label Detector | Only drinks with existing images are loaded")
