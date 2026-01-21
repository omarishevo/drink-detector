import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import pandas as pd

st.set_page_config(page_title="🥤 Drink Detector & CSV Generator", layout="wide")
st.title("🥤 Drink Label Detector with Complete Database")

# -------------------------------
# Step 1: Load the comprehensive drink database
# -------------------------------
@st.cache_data
def load_drink_database():
    """Load the complete drink labels CSV database"""
    # This would normally load from your drink_labels_brands.csv file
    # For now, we'll create the data structure based on the CSV
    data = {
        'Category': ['Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 
                     'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic',
                     'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Alcoholic', 'Alcoholic',
                     'Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic', 'Non-Alcoholic'],
        'Type': ['Soft Drink', 'Soft Drink', 'Energy Drink', 'Soft Drink', 'Soft Drink',
                 'Energy Drink', 'Juice', 'Water', 'Tea', 'Coffee',
                 'Soft Drink', 'Energy Drink', 'Juice', 'Beer', 'Beer',
                 'Liqueur', 'Water', 'Soft Drink', 'Water', 'Tea'],
        'Subtype': ['Cola', 'Cola', 'Regular', 'Lemon-Lime', 'Orange Soda',
                    'Regular', 'Orange Juice', 'Mineral Water', 'Iced Tea', 'Chocolate Drink',
                    'Lemon-Lime', 'Sports Drink', 'Orange Juice', 'Lager', 'Stout',
                    'Cream Liqueur', 'Purified Water', 'Ginger Ale', 'Spring Water', 'Black Tea'],
        'Brand': ['Coca-Cola', 'Pepsi', 'Red Bull', 'Sprite', 'Fanta',
                  'Monster', 'Minute Maid', 'Dasani', 'Lipton', 'Milo',
                  '7UP', 'Lucozade', 'Tropicana', 'Heineken', 'Guinness',
                  'Baileys', 'Aquafina', 'Schweppes', 'Nestle', 'Lipton'],
        'Label': ['Carbonated Soft Drink', 'Cola Carbonated Soft Drink', 'Energy Drink', 
                  'Lemon-Lime Flavored Soda', 'Orange Flavored Soft Drink',
                  'Energy Drink', 'Premium Orange Juice', 'Purified Water', 
                  'Iced Tea', 'Chocolate Malt Drink',
                  'Lemon Lime Soda', 'Energy Drink', '100% Pure Orange Juice', 
                  'Premium Lager Beer', 'Draught Stout',
                  'Irish Cream', 'Purified Drinking Water', 'Ginger Ale', 
                  'Pure Life Water', 'Yellow Label Tea']
    }
    
    # Sample image URLs (using Imgur for stability)
    image_urls = {
        "Coca-Cola": "https://i.imgur.com/u6jhjJW.jpg",
        "Pepsi": "https://i.imgur.com/7Z7FjQv.jpg",
        "Red Bull": "https://i.imgur.com/2j1Nsdn.jpg",
        "Sprite": "https://i.imgur.com/6fOeJ4K.jpg",
        "Fanta": "https://i.imgur.com/g3cqTjB.jpg",
        "Monster": "https://i.imgur.com/q8b3bQX.jpg",
        "Minute Maid": "https://i.imgur.com/Df3tEmk.jpg",
        "Dasani": "https://i.imgur.com/R2krkVr.jpg",
        "Lipton": "https://i.imgur.com/7kIYw0v.jpg",
        "Milo": "https://i.imgur.com/NnJc5gK.jpg",
        "7UP": "https://i.imgur.com/3xQ9s5x.jpg",
        "Lucozade": "https://i.imgur.com/5cUoFkg.jpg",
        "Tropicana": "https://i.imgur.com/1D8ZxjM.jpg",
        "Heineken": "https://i.imgur.com/3bI7tGb.jpg",
        "Guinness": "https://i.imgur.com/8O1r2Qo.jpg",
        "Baileys": "https://i.imgur.com/nR3e2Yv.jpg",
        "Aquafina": "https://i.imgur.com/w8uZ1vN.jpg",
        "Schweppes": "https://i.imgur.com/Gh5XQ3K.jpg",
        "Nestle": "https://i.imgur.com/VGQf6Wz.jpg",
    }
    
    df = pd.DataFrame(data)
    return df, image_urls

# Load the database
drinks_df, image_urls = load_drink_database()

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
# Sidebar: Database Statistics
# -------------------------------
with st.sidebar:
    st.header("📊 Database Stats")
    st.metric("Total Drinks", len(drinks_df))
    st.metric("Categories", drinks_df['Category'].nunique())
    st.metric("Brands", drinks_df['Brand'].nunique())
    st.metric("Types", drinks_df['Type'].nunique())
    
    st.write("---")
    st.write("### Category Breakdown")
    category_counts = drinks_df['Category'].value_counts()
    for cat, count in category_counts.items():
        st.write(f"**{cat}:** {count}")
    
    st.write("---")
    st.download_button(
        label="📥 Download Full Database CSV",
        data=drinks_df.to_csv(index=False),
        file_name="drink_labels_brands_database.csv",
        mime="text/csv",
        use_container_width=True
    )

# -------------------------------
# Main Content: Tabs for different views
# -------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["🔍 Detect Drink", "📸 Browse Gallery", "📊 Database View", "🔄 Batch Process"])

# TAB 1: Detect Drink
with tab1:
    st.write("### 🔍 Select and Detect a Drink")
    
    # Filter options
    col1, col2 = st.columns(2)
    with col1:
        category_filter = st.selectbox("Filter by Category:", 
                                       ["All"] + list(drinks_df['Category'].unique()))
    with col2:
        type_filter = st.selectbox("Filter by Type:", 
                                   ["All"] + list(drinks_df['Type'].unique()))
    
    # Apply filters
    filtered_df = drinks_df.copy()
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df['Category'] == category_filter]
    if type_filter != "All":
        filtered_df = filtered_df[filtered_df['Type'] == type_filter]
    
    # Select drink
    selected_brand = st.selectbox("Select a drink brand:", filtered_df['Brand'].tolist())
    
    # Get drink details
    drink_info = filtered_df[filtered_df['Brand'] == selected_brand].iloc[0]
    
    # Display results
    col_img, col_info = st.columns([1, 2])
    
    with col_img:
        if selected_brand in image_urls:
            img = load_image_from_url(image_urls[selected_brand])
            if img:
                st.image(img, use_container_width=True)
            else:
                st.info("Image not available")
        else:
            st.info("Image not available for this brand")
    
    with col_info:
        st.write("### 🏷️ Detected Drink Information")
        st.success(f"**Brand:** {drink_info['Brand']}")
        st.write(f"**Label:** {drink_info['Label']}")
        st.write(f"**Category:** {drink_info['Category']}")
        st.write(f"**Type:** {drink_info['Type']}")
        st.write(f"**Subtype:** {drink_info['Subtype']}")
        
        if selected_brand in image_urls:
            st.code(f"Image URL: {image_urls[selected_brand]}", language="text")

# TAB 2: Browse Gallery
with tab2:
    st.write("### 📸 Drink Image Gallery")
    st.info("Browse all available drink images in the database")
    
    num_cols = 4
    brands_with_images = [b for b in drinks_df['Brand'].unique() if b in image_urls]
    
    for i in range(0, len(brands_with_images), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            if i + j < len(brands_with_images):
                brand = brands_with_images[i + j]
                with col:
                    img = load_image_from_url(image_urls[brand])
                    if img:
                        st.image(img, caption=brand, use_container_width=True)
                        drink_detail = drinks_df[drinks_df['Brand'] == brand].iloc[0]
                        st.caption(f"{drink_detail['Type']} - {drink_detail['Category']}")

# TAB 3: Database View
with tab3:
    st.write("### 📊 Complete Database View")
    
    # Search functionality
    search_term = st.text_input("🔍 Search drinks:", placeholder="Enter brand, type, or category...")
    
    if search_term:
        search_df = drinks_df[
            drinks_df.apply(lambda row: search_term.lower() in row.to_string().lower(), axis=1)
        ]
        st.write(f"Found {len(search_df)} results")
        st.dataframe(search_df, use_container_width=True)
    else:
        st.dataframe(drinks_df, use_container_width=True)
    
    # Export filtered data
    csv_data = search_df.to_csv(index=False) if search_term else drinks_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Displayed Data as CSV",
        data=csv_data,
        file_name="filtered_drinks.csv",
        mime="text/csv"
    )

# TAB 4: Batch Process
with tab4:
    st.write("### 🔄 Batch Process All Drinks")
    st.info("Process all drinks in the database and check image availability")
    
    if st.button("▶️ Process All Drinks", type="primary"):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        results = []
        total = len(drinks_df)
        
        for idx, row in drinks_df.iterrows():
            brand = row['Brand']
            status_text.text(f"Processing {brand}... ({idx + 1}/{total})")
            
            # Check if image exists
            has_image = brand in image_urls
            image_status = "✅ Available" if has_image else "❌ No Image"
            
            # Try to load image if URL exists
            load_status = "N/A"
            if has_image:
                img = load_image_from_url(image_urls[brand])
                load_status = "✅ Loaded" if img else "❌ Failed to Load"
            
            results.append({
                "Brand": brand,
                "Category": row['Category'],
                "Type": row['Type'],
                "Label": row['Label'],
                "Image Status": image_status,
                "Load Status": load_status
            })
            
            progress_bar.progress((idx + 1) / total)
        
        status_text.text("Processing complete!")
        
        # Display results
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)
        
        # Summary
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Processed", len(results_df))
        with col2:
            images_available = len([r for r in results if "Available" in r["Image Status"]])
            st.metric("Images Available", images_available)
        with col3:
            successfully_loaded = len([r for r in results if "Loaded" in r["Load Status"]])
            st.metric("Successfully Loaded", successfully_loaded)
        
        # Download results
        st.download_button(
            label="📥 Download Processing Results",
            data=results_df.to_csv(index=False),
            file_name="batch_processing_results.csv",
            mime="text/csv"
        )

# -------------------------------
# Footer
# -------------------------------
st.write("---")
st.caption("🥤 Drink Detector & Database System | Powered by Streamlit & Comprehensive CSV Database")
