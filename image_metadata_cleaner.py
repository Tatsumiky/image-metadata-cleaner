import os
import io
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog, simpledialog


def get_metadata_summary(img):
    findings = {}

    for key, value in img.info.items():
        if key.lower() in ('exif', 'icc_profile'):
            continue
        text = str(value)
        findings[key] = text[:200] + ('...' if len(text) > 200 else '')

    try:
        exif = img.getexif()
        if exif:
            findings['EXIF'] = {k: str(v)[:100] for k, v in exif.items()}
    except Exception:
        pass

    return findings


def print_metadata(label, img):
    data = get_metadata_summary(img)
    if not data:
        print(f"   {label}: no metadata found.")
        return
    print(f"   {label}: metadata found:")
    for key, value in data.items():
        print(f"     - {key}: {value}")


def clean_images_to_png():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    print("Select one or more images to clean (they will be saved as PNG)...")

    file_paths = filedialog.askopenfilenames(
        parent=root,
        title="Select image files",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png *.webp"),
            ("All Files", "*.*")
        ]
    )

    if not file_paths:
        print("No files selected. Script cancelled.")
        root.destroy()
        return

    prefix = simpledialog.askstring(
        "File prefix",
        "Enter the prefix for the cleaned files (e.g.: Clean):",
        initialvalue="Clean",
        parent=root
    )
    if prefix is None:
        print("Operation cancelled by user.")
        root.destroy()
        return
    prefix = "".join(c for c in prefix.strip() if c not in '\\/:*?"<>|')
    if prefix and not prefix.endswith("_"):
        prefix += "_"

    print("Select the folder where the cleaned images will be saved...")
    output_dir = filedialog.askdirectory(
        parent=root,
        title="Select destination folder"
    )
    if not output_dir:
        print("No folder selected. Script cancelled.")
        root.destroy()
        return

    for file_path in file_paths:
        try:
            with Image.open(file_path) as img:
                print(f"\nChecking: {os.path.basename(file_path)}")
                print_metadata("Before cleaning", img)

                img = ImageOps.exif_transpose(img)

                if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                    print(f"-> {os.path.basename(file_path)} has transparency. Converting to RGB...")
                    img = img.convert('RGBA')
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[3])
                    img = background
                elif img.mode != 'RGB':
                    img = img.convert('RGB')

                temp_jpeg_stream = io.BytesIO()
                img.save(temp_jpeg_stream, 'JPEG', quality=95, subsampling=0)
                temp_jpeg_stream.seek(0)

                with Image.open(temp_jpeg_stream) as clean_img:
                    name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
                    new_file_name = f"{prefix}{name_without_ext}.png"
                    new_file_path = os.path.join(output_dir, new_file_name)

                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_name = f"{prefix}{name_without_ext}_{counter}.png"
                        new_file_path = os.path.join(output_dir, new_file_name)
                        counter += 1

                    clean_img.save(new_file_path, 'PNG')
                    print_metadata("After cleaning", clean_img)
                    print(f"[OK] Cleaned: {os.path.basename(file_path)} -> {new_file_path}")

        except Exception as e:
            print(f"[ERROR] Could not process '{file_path}': {e}")

    print("\n--- Done ---")
    print(f"All selected images have been processed and saved to: {output_dir}")

    root.destroy()


if __name__ == "__main__":
    clean_images_to_png()