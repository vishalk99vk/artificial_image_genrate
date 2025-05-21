import streamlit as st
from PIL import Image, UnidentifiedImageError
import os
import tempfile
import zipfile

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

def load_and_show_first_image(image_paths, caption):
    if not image_paths:
        st.warning("No valid images found.")
        return
    try:
        img_path = image_paths[0]
        img = Image.open(img_path)
        st.image(img, caption=f"{caption} - {os.path.basename(img_path)}")
    except UnidentifiedImageError:
        st.error(f"Cannot identify image file: {img_path}")
    except Exception as e:
        st.error(f"Error loading image: {e}")

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
                load_and_show_first_image(product_images, "Product Image")

    elif choice == "Crop Shelf Textures":
        st.header("Crop Shelf Textures")
        uploaded = st.file_uploader("Upload shelf images (zip)", type=["zip"])
        if uploaded:
            with tempfile.TemporaryDirectory() as temp_dir:
                unzip_uploaded_zip(uploaded, temp_dir)
                st.write(f"Extracted files/folders: {os.listdir(temp_dir)}")
                shelf_images = find_images_recursively(temp_dir)
                st.write(f"Found shelf images: {len(shelf_images)}")
                load_and_show_first_image(shelf_images, "Shelf Texture")

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
                # Just show first image of each folder as demo:
                load_and_show_first_image(product_images, "Product Image")
                load_and_show_first_image(shelf_textures, "Shelf Texture")

if __name__ == "__main__":
    main()
