from PIL import Image
import os
import glob

def center_crop(im, new_width=None, new_height=None):
    width, height = im.size  # Get dimensions
    left = round((width - new_width) / 2)
    top = round((height - new_height) / 2)
    x_right = round(width - new_width) - left
    x_bottom = round(height - new_height) - top
    right = width - x_right
    bottom = height - x_bottom
    # Crop the center of the image
    return im.crop((left, top, right, bottom))

for filePath in glob.glob('numbers/*.png'):
    filename = os.path.split(filePath)[1]
    im = Image.open(filePath)
    cropped = center_crop(im, 50, 50)
    print(f"cropped/{filename}")
    cropped.save(f"cropped/{filename}")
