import streamlit as st
from PIL import Image
import os
import tempfile
import zipfile
import random
from io import BytesIO

# ---- Utility functions ----
def unzip_uploaded_zip(uploaded_zip, extract_to):
    with zipfile.ZipFile(uploaded_zip) as z:
        z.extractall(extract_to)

def find_images_recursively(folder):
    valid_exts = ('.png', '.jpg', '.jpeg')
    image_paths = []
    for root, _, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(valid_exts):
                image_paths.append(os.path.join(root, file))
    return image_paths

# ---- Stub processing functions (replace with your actual logic) ----
def batch_remove_background_stub(images):
    st.write(f"Removing backgrounds for {len(images)} images (stub).")
    # Example: just show the first image
    if images:
        img = Image.open(images[0])
        st.image(img, caption="Example product image")

def crop_shelf_texture_stub(images):
    st.write(f"Cropping shelf textures for {len(images)} images (stub).")
    if images:
        img = Image.open(images[0])
        st.image(img, caption="Example shelf texture")

def generate_shelf_stub(products, textures):
    st.write(f"Generating synthetic shelf with {len(products)} products and {len(textures)} textures (stub).")
    # Create a blank dummy image for demo
    img = Image.new("RGB", (800, 600), color=(200, 200, 200))
    st.image(img, caption="Synthetic Shelf Example")

# ---- Main Streamlit app ----
def main():
    st.title("Shelf Synthetic Image Generator")

    menu = ["Batch Remove Background", "Crop Shelf Textures", "Generate Synthetic Shelf"]
    choice = st.sidebar.selectbox("Select Task", menu)

    if choice == "Batch Remove Background":
        st.header("Batch Remove Background")
        uploaded = st.file_uploader("Upload product images (zip)", type=["zip"])
        if uploaded:
            with tempfile.TemporaryDirectory() as temp_dir:
                unzip_uploaded_zip(uploaded, temp_dir)
                st.write(f"Extracted files/folders: {os.listdir(temp_dir)}")
                product_images = find_images_recursively(temp_dir)
                st.write(f"Found product images: {len(product_images)}")
                batch_remove_background_stub(product_images)

    elif choice == "Crop Shelf Textures":
        st.header("Crop Shelf Textures")
        uploaded = st.file_uploader("Upload shelf images (zip)", type=["zip"])
        if uploaded:
            with tempfile.TemporaryDirectory() as temp_dir:
                unzip_uploaded_zip(uploaded, temp_dir)
                st.write(f"Extracted files/folders: {os.listdir(temp_dir)}")
                shelf_images = find_images_recursively(temp_dir)
                st.write(f"Found shelf images: {len(shelf_images)}")
                crop_shelf_texture_stub(shelf_images)

    elif choice == "Generate Synthetic Shelf":
        st.header("Generate Synthetic Shelf")
        uploaded_products = st.file_uploader("Upload product images (zip)", type=["zip"], key="prod")
        uploaded_textures = st.file_uploader("Upload shelf textures (zip)", type=["zip"], key="texture")
        if uploaded_products and uploaded_textures:
            with tempfile.TemporaryDirectory() as prod_dir, tempfile.TemporaryDirectory() as tex_dir:
                unzip_uploaded_zip(uploaded_products, prod_dir)
                unzip_uploaded_zip(uploaded_textures, tex_dir)
                product_images = find_images_recursively(prod_dir)
                shelf_textures = find_images_recursively(tex_dir)
                st.write(f"Found {len(product_images)} product images and {len(shelf_textures)} shelf textures")
                generate_shelf_stub(product_images, shelf_textures)

if __name__ == "__main__":
    main()
