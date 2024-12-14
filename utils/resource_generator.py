import os
from PIL import Image, ImageDraw, ImageFont

class ResourceGenerator:
    def __init__(self):
        os.makedirs("assets/images/vocab", exist_ok=True)

    def generate_placeholder_image(self, text, output_path):
        # Create a simple image with white background and black text
        img = Image.new("RGB", (300, 300), "white")
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 30)
        except:
            font = ImageFont.load_default()

        # Use textbbox to determine the width and height of the text
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]

        # Calculate coordinates to center the text in the image
        x = (300 - w) // 2
        y = (300 - h) // 2

        draw.text((x, y), text, fill="black", font=font)
        img.save(output_path)
        return output_path