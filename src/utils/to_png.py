import json
from PIL import Image, ImageDraw, ImageFont

def json_to_png(json_path, png_path, font_path=None, font_size=16,
                padding=20, bg_color="white", text_color="black"):

    # --- Load JSON file ---
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Pretty print JSON text
    json_text = json.dumps(data, indent=4, ensure_ascii=False)

    # --- Set up font ---
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # --- Determine image size using multiline_textbbox ---
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)

    # bbox = (left, top, right, bottom)
    bbox = draw.multiline_textbbox((0, 0), json_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img_width = text_width + padding * 2
    img_height = text_height + padding * 2

    # --- Create final image ---
    img = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    # Draw text
    draw.multiline_text((padding, padding), json_text, font=font, fill=text_color)

    # Save PNG
    img.save(png_path)
    print(f"Saved PNG to: {png_path}")


def text_to_png(text_path, png_path, font_path=None, font_size=16,
                padding=20, bg_color="white", text_color="black"):

    # --- Load text file ---
    with open(text_path, "r", encoding="utf-8") as f:
        text = f.read()

    # --- Set up font ---
    if font_path:
        font = ImageFont.truetype(font_path, font_size)
    else:
        font = ImageFont.load_default()

    # --- Measure text size using multiline_textbbox ---
    temp_img = Image.new("RGB", (1, 1))
    draw = ImageDraw.Draw(temp_img)

    bbox = draw.multiline_textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    img_width = text_width + padding * 2
    img_height = text_height + padding * 2

    # --- Create final image ---
    img = Image.new("RGB", (img_width, img_height), color=bg_color)
    draw = ImageDraw.Draw(img)

    draw.multiline_text((padding, padding), text, font=font, fill=text_color)

    img.save(png_path)
    print(f"Saved PNG to: {png_path}")


# Example
if __name__ == "__main__":
    text_to_png("spec.txt", "spec.png")
