import streamlit as st
from PIL import Image
import pandas as pd
import os

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="🥤 Drink Label Detector",
    layout="wide"
)

st.title("🥤 Drink Label Detector & CSV Generator")

IMAGE_DIR = "images"

# --------------------------------------------------
# LOAD DATABASE
# --------------------------------------------------
@st.cache_data
def load_drink_database():
    data = {
        "Category": [
            "Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic","Non-Alcoholic",
            "Energy Drink","Juice","Water","Tea","Coffee"
        ],
        "Type": [
            "Soft Drink","Soft Drink","Energy Drink","Soft Drink","Soft Drink",
            "Energy Drink","Juice","Water","Tea","Chocolate Drink"
        ],
        "Subtype": [
            "Cola","Cola","Regular","Lemon-Lime","Orange Soda",
            "Regular","Orange Juice","Mineral Water","Iced Tea","Malt Drink"
        ],
        "Brand": [
            "Coca-Cola","Pepsi","Red Bull","Sprite","Fanta",
            "Monster","Minute Maid","Dasani","Lipton","Milo"
        ],
        "Label": [
            "Carbonated Soft Drink","Cola Carbonated Drink","Energy Drink",
            "Lemon Soda","Orange Soda","Energy Drink",
            "Fruit Juice","Drinking Water","Iced Tea","Chocolate Drink"
        ]
    }

    image_files = {
        "Coca-Cola": "cocacola.jpg",
        "Pepsi": "pepsi.jpg",
        "Red Bull": "redbull.jpg",
        "Sprite": "sprite.jpg",
        "Fanta": "fanta.jpg",
        "Monster": "monster.jpg",
        "Minute Maid": "minute maid.jpg",
        "Dasani": "Dasani.jpg",
        "Lipton": "lipton.jpg",
        "Milo": "milo.jpg"
    }

    image_paths = {
        brand: os.path.join(IMAGE_DIR, file)
        for brand, file in image_files.items()
    }

    return pd.DataFrame(data), image_paths


drinks_df, image_paths = load_drink_database()

# --------------------------------------------------
# IMAGE LOADER (SAFE)
# --------------------------------------------------
@st.cache_data
def load_image(path):
    try:
        if os.path.exists(path):
            return Image.open(path).convert("RGB")
        return None
    except Exception:
        return None

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.header("📊 Database Stats")
    st.metric("Total Drinks", len(drinks_df))
    st.metric("Categories", drinks_df["Category"].nunique())
    st.metric("Brands", drinks_df["Brand"].nunique())

    found = sum(os.path.exists(p) for p in image_paths.values())
    missing = len(image_paths) - found

    st.write("---")
    st.metric("Images Found", found)
    st.metric("Images Missing", missing)

    st.write("---")
    st.download_button(
        "📥 Download Full CSV",
        drinks_df.to_csv(index=False),
        "drink_labels_database.csv",
        "text/csv"
    )

# --------------------------------------------------
# TABS
# --------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "🔍 Detect Drink",
    "📸 Gallery",
    "📊 Database"
])

# --------------------------------------------------
# TAB 1: DETECT
# --------------------------------------------------
with tab1:
    st.subheader("🔍 Detect a Drink")

    category = st.selectbox(
        "Filter by Category",
        ["All"] + sorted(drinks_df["Category"].unique())
    )

    filtered_df = drinks_df if category == "All" else drinks_df[drinks_df["Category"] == category]

    brand = st.selectbox("Select Brand", filtered_df["Brand"])

    drink = filtered_df[filtered_df["Brand"] == brand].iloc[0]

    col1, col2 = st.columns([1, 2])

    with col1:
        img = load_image(image_paths.get(brand, ""))
        if img:
            st.image(img, use_container_width=True)
        else:
            st.warning("⚠️ Image not available")

    with col2:
        st.success(f"**Brand:** {drink['Brand']}")
        st.write(f"**Category:** {drink['Category']}")
        st.write(f"**Type:** {drink['Type']}")
        st.write(f"**Subtype:** {drink['Subtype']}")
        st.write(f"**Label:** {drink['Label']}")

# --------------------------------------------------
# TAB 2: GALLERY
# --------------------------------------------------
with tab2:
    st.subheader("📸 Drink Gallery")

    cols = st.columns(4)
    for idx, brand in enumerate(drinks_df["Brand"]):
        with cols[idx % 4]:
            img = load_image(image_paths.get(brand, ""))
            if img:
                st.image(img, caption=brand, use_container_width=True)
            else:
                st.error(brand)

# --------------------------------------------------
# TAB 3: DATABASE
# --------------------------------------------------
with tab3:
    st.subheader("📊 Full Database")

    search = st.text_input("🔍 Search")

    if search:
        df = drinks_df[
            drinks_df.apply(
                lambda row: search.lower() in row.to_string().lower(),
                axis=1
            )
        ]
    else:
        df = drinks_df

    st.dataframe(df, use_container_width=True)

    st.download_button(
        "📥 Download Displayed Data",
        df.to_csv(index=False),
        "filtered_drinks.csv",
        "text/csv"
    )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.write("---")
st.caption("🥤 Drink Label Detector | Streamlit Deployment Ready")

