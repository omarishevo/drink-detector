import streamlit as st
from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import pandas as pd
import os

st.set_page_config(page_title="🥤 Drink Detector & CSV Generator", layout="wide")
st.title("🥤 Drink Label Detector with Complete Database")

# -------------------------------
# Step 1: Load the comprehensive drink database
# -------------------------------
@st.cache_data
def load_drink_database():
    """Load the complete drink labels CSV database"""
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
                  'Baileys', 'Aquafina', 'Schweppes', 'Nestle', 'Lipton Tea'],
        'Label': ['Carbonated Soft Drink', 'Cola Carbonated Soft Drink', 'Energy Drink', 
                  'Lemon-Lime Flavored Soda', 'Orange Flavored Soft Drink',
                  'Energy Drink', 'Premium Orange Juice', 'Purified Water', 
                  'Iced Tea', 'Chocolate Malt Drink',
                  'Lemon Lime Soda', 'Energy Drink', '100% Pure Orange Juice', 
                  'Premium Lager Beer', 'Draught Stout',
                  'Irish Cream', 'Purified Drinking Water', 'Ginger Ale', 
                  'Pure Life Water', 'Yellow Label Tea']
    }
    
    # Image paths - REPLACE THESE WITH YOUR LOCAL FILE PATHS
    # Format: r"C:\path\to\your\image.jpg" or just use forward slashes
    image_paths = {
        "Coca-Cola": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\cocacola.jpg",
        "Pepsi": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\pepsi.jpg",
        "Red Bull": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\redbull.jpg",
        "Sprite": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\sprite.jpg",
        "Fanta": r""C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\fanta.jpg",
        "Monster": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\monster.jpg",
        "Minute Maid": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\minutemaid.jpg",
        "Dasani": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\dasani.jpg",
        "Lipton": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\lipton.jpg",
        "Milo": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\milo.jpg",
        "7UP": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\7up.jpg",
        "Lucozade": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\lucozade.jpg",
        "Tropicana": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\tropicana.jpg",
        "Heineken": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\heineken.jpg",
        "Guinness": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\guinness.jpg",
        "Baileys": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\baileys.jpg",
        "Aquafina": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\aquafina.jpg",
        "Schweppes": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\schweppes.jpg",
        "Nestle": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\nestle.jpg",
        "Lipton Tea": r"C:\Users\Administrator\OneDrive\Documentos\Imagens\abkul.nn\lipton_tea.jpg",
    }
    
    df = pd.DataFrame(data)
    return df, image_paths

# Load the database
drinks_df, image_paths = load_drink_database()

# -------------------------------
# Helper function to load images from local file paths
# -------------------------------
@st.cache_data
def load_image_from_path(path):
    """Load image from local file path with caching"""
    try:
        if os.path.exists(path):
            img = Image.open(path)
            return img
        else:
            return None
    except (FileNotFoundError, UnidentifiedImageError, PermissionError) as e:
        return None

# -------------------------------
# Sidebar: Database Statistics & Image Path Manager
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
    
    # Image status check
    st.write("### 📷 Image Status")
    images_found = sum(1 for path in image_paths.values() if os.path.exists(path))
    images_missing = len(image_paths) - images_found
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Found", images_found, delta_color="normal")
    with col2:
        st.metric("Missing", images_missing, delta_color="inverse")
    
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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Detect Drink", 
    "📸 Browse Gallery", 
    "📊 Database View", 
    "🔄 Batch Process",
    "⚙️ Image Path Manager"
])

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
        if selected_brand in image_paths:
            img_path = image_paths[selected_brand]
            img = load_image_from_path(img_path)
            if img:
                st.image(img, use_container_width=True)
                st.caption(f"✅ Image loaded successfully")
            else:
                st.warning(f"⚠️ Image not found at path")
                st.caption(f"Please check: {img_path}")
        else:
            st.info("Image path not configured for this brand")
    
    with col_info:
        st.write("### 🏷️ Detected Drink Information")
        st.success(f"**Brand:** {drink_info['Brand']}")
        st.write(f"**Label:** {drink_info['Label']}")
        st.write(f"**Category:** {drink_info['Category']}")
        st.write(f"**Type:** {drink_info['Type']}")
        st.write(f"**Subtype:** {drink_info['Subtype']}")
        
        if selected_brand in image_paths:
            st.write("### 📁 Image File Path")
            st.code(image_paths[selected_brand], language="text")
            
            # Check if file exists
            if os.path.exists(image_paths[selected_brand]):
                file_size = os.path.getsize(image_paths[selected_brand]) / 1024  # KB
                st.success(f"✅ File exists ({file_size:.2f} KB)")
            else:
                st.error("❌ File not found at this path")

# TAB 2: Browse Gallery
with tab2:
    st.write("### 📸 Drink Image Gallery")
    st.info("Browse all available drink images in the database")
    
    num_cols = 4
    brands_with_images = list(drinks_df['Brand'].unique())
    
    for i in range(0, len(brands_with_images), num_cols):
        cols = st.columns(num_cols)
        for j, col in enumerate(cols):
            if i + j < len(brands_with_images):
                brand = brands_with_images[i + j]
                with col:
                    if brand in image_paths:
                        img = load_image_from_path(image_paths[brand])
                        if img:
                            st.image(img, caption=brand, use_container_width=True)
                            drink_detail = drinks_df[drinks_df['Brand'] == brand].iloc[0]
                            st.caption(f"{drink_detail['Type']} - {drink_detail['Category']}")
                        else:
                            st.error(f"❌ {brand}")
                            st.caption("Image not found")
                    else:
                        st.warning(f"⚠️ {brand}")
                        st.caption("No path configured")

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
            
            # Check if image path exists
            has_path = brand in image_paths
            path_status = "✅ Path Configured" if has_path else "❌ No Path"
            
            # Try to load image if path exists
            load_status = "N/A"
            file_exists = "N/A"
            file_size = "N/A"
            
            if has_path:
                path = image_paths[brand]
                if os.path.exists(path):
                    file_exists = "✅ File Found"
                    size = os.path.getsize(path) / 1024
                    file_size = f"{size:.2f} KB"
                    
                    img = load_image_from_path(path)
                    load_status = "✅ Loaded" if img else "❌ Failed to Load"
                else:
                    file_exists = "❌ File Not Found"
                    load_status = "❌ Cannot Load"
            
            results.append({
                "Brand": brand,
                "Category": row['Category'],
                "Type": row['Type'],
                "Label": row['Label'],
                "Path Status": path_status,
                "File Status": file_exists,
                "Load Status": load_status,
                "File Size": file_size
            })
            
            progress_bar.progress((idx + 1) / total)
        
        status_text.text("Processing complete!")
        
        # Display results
        results_df = pd.DataFrame(results)
        st.dataframe(results_df, use_container_width=True)
        
        # Summary
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Processed", len(results_df))
        with col2:
            paths_configured = len([r for r in results if "Configured" in r["Path Status"]])
            st.metric("Paths Configured", paths_configured)
        with col3:
            files_found = len([r for r in results if "File Found" in r["File Status"]])
            st.metric("Files Found", files_found)
        with col4:
            successfully_loaded = len([r for r in results if r["Load Status"] == "✅ Loaded"])
            st.metric("Successfully Loaded", successfully_loaded)
        
        # Download results
        st.download_button(
            label="📥 Download Processing Results",
            data=results_df.to_csv(index=False),
            file_name="batch_processing_results.csv",
            mime="text/csv"
        )

# TAB 5: Image Path Manager
with tab5:
    st.write("### ⚙️ Image Path Manager")
    st.info("View and copy image file paths for all drinks")
    
    st.write("#### 📋 All Image Paths")
    st.write("Copy and paste these paths to configure your image locations:")
    
    # Create a dataframe with paths
    path_data = []
    for brand, path in image_paths.items():
        exists = os.path.exists(path)
        status = "✅ Found" if exists else "❌ Missing"
        path_data.append({
            "Brand": brand,
            "File Path": path,
            "Status": status
        })
    
    paths_df = pd.DataFrame(path_data)
    st.dataframe(paths_df, use_container_width=True)
    
    st.write("---")
    st.write("#### 📝 Path Template")
    st.write("Use this template to update your image paths in the code:")
    
    template = """
# Copy this into the load_drink_database() function:
image_paths = {
"""
    for brand in drinks_df['Brand'].unique():
        template += f'    "{brand}": r"C:\\path\\to\\your\\images\\{brand.lower().replace(" ", "_")}.jpg",\n'
    template += "}"
    
    st.code(template, language="python")
    
    st.write("---")
    st.write("#### 💡 Tips:")
    st.write("1. Use the `r` prefix before strings to handle Windows paths correctly")
    st.write("2. Use double backslashes `\\\\` or forward slashes `/` in paths")
    st.write("3. Example: `r'C:\\Users\\Admin\\Images\\coca-cola.jpg'`")
    st.write("4. Place all images in one folder for easier management")

# -------------------------------
# Footer
# -------------------------------
st.write("---")
st.caption("🥤 Drink Detector & Database System | Local File Path Support | Powered by Streamlit")
