from PIL import Image, ImageEnhance, ImageFilter
import os
from pathlib import Path

# Define input and output directories
path = Path("C:/Users/harij/PycharmProjects/Code_Alpha/PythonScript/imgs")
pathOut = Path("C:/Users/harij/PycharmProjects/Code_Alpha/PythonScript/editedImgs")

# Ensure the output directory exists
pathOut.mkdir(parents=True, exist_ok=True)

# Iterate over all files in the input directory
for filename in os.listdir(path):
    file_path = path / filename  # Full path to the image file

    if file_path.is_file() and file_path.suffix.lower() in {".png", ".jpg", ".jpeg"}:  # Check for valid image files
        img = Image.open(file_path)

        # Apply edits: sharpening, black & white conversion, and rotation
        edit = img.filter(ImageFilter.SHARPEN).convert('L').rotate(-90)

        # Enhance contrast
        factor = 1.5
        enhancer = ImageEnhance.Contrast(edit)
        edit = enhancer.enhance(factor)

        # Save the edited image
        clean_name = file_path.stem  # Get the file name without extension
        output_path = pathOut / f"{clean_name}_edited.jpg"
        edit.save(output_path)

        print(f"Processed and saved: {output_path}")
