import streamlit as st
from PIL import Image
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision import models
import os
import gdown

st.set_page_config(page_title="🥤 Drink Detector", layout="centered")
st.title("🥤 Drink Label Detection System (PyTorch Version)")

# -------------------------------
# Download model (optional)
# -------------------------------
MODEL_PATH = "drink_detector.pt"
DRIVE_ID = "YOUR_MODEL_FILE_ID"

if not os.path.exists(MODEL_PATH):
    url = f"https://drive.google.com/uc?id={DRIVE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

# -------------------------------
# Load PyTorch model
# -------------------------------
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = torch.load(MODEL_PATH, map_location=device)
model.eval()

# -------------------------------
# Load Labels
# -------------------------------
with open("labels.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

# -------------------------------
# Image preprocessing
# -------------------------------
preprocess = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def predict(image: Image.Image):
    img = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(img)
        probs = torch.softmax(outputs, dim=1)
        confidence, idx = torch.max(probs, dim=1)
    return class_names[idx.item()], confidence.item()

# -------------------------------
# Upload image
# -------------------------------
uploaded_file = st.file_uploader("Upload Drink Image", type=["jpg", "jpeg", "png"])
if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    if st.button("Detect Drink Label"):
        label, conf = predict(image)
        st.success("Detection Complete!")
        st.write(f"### 🏷️ Predicted Drink: **{label}**")
        st.write(f"### 📊 Confidence: **{conf*100:.2f}%**")
