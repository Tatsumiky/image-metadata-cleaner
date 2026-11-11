# Image Metadata Cleaner

A simple Python script that removes metadata (EXIF, embedded text, etc.) from images and saves clean copies as PNG files. It uses pop-up windows, so no coding is needed to run it.

## What it does

- Lets you pick one or more images (JPG, PNG, WEBP)
- Removes metadata such as EXIF data, camera info and embedded text
- Saves clean PNG copies with a custom prefix in a folder of your choice
- Never modifies your original files

## Limitations

- **Re-encoding is lossy.** Each image is passed through a high-quality JPEG step before being saved as PNG. This removes metadata and disturbs most simple data hidden in pixels, but it can add slight compression artifacts and make files larger than the originals.
- **Color profiles (ICC) are removed**, so images with wide color gamuts may look slightly different.
- **No guarantee against advanced steganography.** This helps against simple cases only.
- **Transparent images get a white background.**
- **Animated images (GIF, animated WebP)** keep only the first frame.

## Requirements

- Windows with [Python 3](https://www.python.org/downloads/) installed
- The Pillow library (installed in Step 4 below)

## Setup (one time only)

**Step 1: Download the script**
Click `image_metadata_cleaner.py` in this repository, then click the download button. Save it in an easy-to-find folder, for example `ImageCleaner` on your Desktop.

**Step 2: Open the Command Prompt**
Press **Windows key + R**, type `cmd` and press **Enter**.

**Step 3: Check that Python works**

```
python --version
```

- If you see something like `Python 3.12.x`, continue.
- If you see "python is not recognized", try `py --version`. If that works, use `py` instead of `python` in all the steps below.
- If neither works, reinstall Python and check **"Add python.exe to PATH"** on the first installer screen.

**Step 4: Install the image library**

```
pip install pillow
```

If `pip` is not recognized, use:

```
python -m pip install pillow
```

## How to use

**Step 1: Open the Command Prompt inside your folder**
Open the folder with `image_metadata_cleaner.py` in File Explorer, click the address bar, type `cmd` and press **Enter**.

**Step 2: Start the script**

```
python image_metadata_cleaner.py
```

**Step 3: Follow the pop-up windows**

1. **Select your images.** Hold **Ctrl** to select several.
2. **Type a prefix.** It is added to the start of each new file name. Example: with the prefix `Clean`, `photo.jpg` becomes `Clean_photo.png`.
3. **Choose the destination folder** where the cleaned images will be saved.

When you see `--- Done ---`, you are finished.

## Troubleshooting

| Problem | Fix |
|---|---|
| `python is not recognized` | Try `py image_metadata_cleaner.py`. If that fails, reinstall Python with "Add python.exe to PATH" checked. |
| `ModuleNotFoundError: No module named 'PIL'` | Run `pip install pillow` again (Setup, Step 4). |
| `can't open file ... No such file or directory` | You are in the wrong folder. Redo "How to use", Step 1. |
| No window appears | The pop-up may be behind other windows. Check the taskbar. |
| File is named `image_metadata_cleaner.py.txt` | Rename it and remove `.txt`. In File Explorer, enable **View > Show > File name extensions**. |

## License

MIT
