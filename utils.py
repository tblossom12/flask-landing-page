from PIL import Image, ImageDraw, ImageFont, ImageColor
import os
import textwrap
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime


def save_to_google_sheet(data):
    creds_path = os.environ.get("GOOGLE_CREDS_PATH", ".gitignore/google-creds.json")
    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    creds = Credentials.from_service_account_file(creds_path, scopes=scope)
    client = gspread.authorize(creds)
    try:
        sheet = client.open_by_key("1lExmF-PJY7k9b25tIAr3_NmE0tD5ozw1uZcwE6Tb4ec").sheet1
        row = [
            data["name"],
            data["email"],
            data["phone"],
            data["claim"],
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data["landing"]
        ]
        sheet.append_row(row)    
    except Exception as e:
        raise

def recolor_logo(path, color="#FFFFFF"):
    logo = Image.open(path).convert("RGBA")
    datas = logo.getdata()

    new_data = []
    for item in datas:
        if item[3] > 0:  # Only recolor non-transparent pixels
            new_data.append((*ImageColor.getrgb(color), item[3]))
        else:
            new_data.append(item)

    logo.putdata(new_data)
    return logo


# def generate_ad_image(para1, para2, sentence1, sentence2, company):
#     width, height = 1080, 1080
#     img = Image.new("RGB", (width, height), color="#0070C0")
#     draw = ImageDraw.Draw(img)

#     base_dir = os.path.dirname(__file__)
#     font_path = os.path.join(base_dir, "static", "fonts", "Inter-Bold.ttf")

#     try:
#         bold_font = ImageFont.truetype(font_path, size=56)
#         normal_font = ImageFont.truetype(font_path, size=46)
#         small_font = ImageFont.truetype(font_path, size=18)
#     except:
#         bold_font = normal_font = small_font = ImageFont.load_default()

#     primary_color = "#222"
#     border_color = "#0070C0"
#     off_color = "#0070C0"
#     footer_color = "white"

#     y = 100
#     content_width = width - 100
#     lines1 = textwrap.wrap(para1, width=30)
#     lines2 = textwrap.wrap(para2, width=40)

#     # Compute box height
#     block_height = 0
#     for line in lines1:
#         bbox = draw.textbbox((0, 0), line, font=bold_font)
#         block_height += bbox[3] - bbox[1] + 15
#     for line in lines2:
#         bbox = draw.textbbox((0, 0), line, font=normal_font)
#         block_height += bbox[3] - bbox[1] + 15

#     box_top = y - 10
#     box_bottom = box_top + block_height + 180
#     draw.rectangle([0, box_top, width, box_bottom], outline=border_color, width=3, fill="white")

#     y += 20

#     for line in lines1:
#         bbox = draw.textbbox((0, 0), line, font=bold_font)
#         draw.text(((width - bbox[2]) / 2, y), line, font=bold_font, fill=off_color)
#         y += bbox[3] - bbox[1] + 15

#     y += 80

#     for line in lines2:
#         bbox = draw.textbbox((0, 0), line, font=normal_font)
#         draw.text(((width - bbox[2]) / 2, y), line, font=normal_font, fill=primary_color)
#         y += bbox[3] - bbox[1] + 15

#     y = box_bottom + 50

#     # Logo
#     logo_path = os.path.join(base_dir, "static", "images", "logo.png")
#     try:
#         logo = recolor_logo(logo_path, color="white")
#         logo_width = 175
#         logo_ratio = logo_width / logo.width
#         logo_height = int(logo.height * logo_ratio)
#         logo = logo.resize((logo_width, logo_height))
#         img.paste(logo, ((width - logo_width) // 2, y), logo)
#         y += logo_height + 30
#     except Exception as e:
#         print("Logo error:", e)

#     for line in textwrap.wrap(sentence1, width=60):
#         bbox = draw.textbbox((0, 0), line, font=small_font)
#         draw.text(((width - bbox[2]) / 2, y), line, font=small_font, fill="white")
#         y += bbox[3] - bbox[1] + 30

#     for line in textwrap.wrap(sentence2, width=60):
#         bbox = draw.textbbox((0, 0), line, font=small_font)
#         draw.text(((width - bbox[2]) / 2, y), line, font=small_font, fill="white")
#         y += bbox[3] - bbox[1] + 10

#     footer_text = footer
#     bbox = draw.textbbox((0, 0), footer_text, font=small_font)
#     draw.text(((width - bbox[2]) / 2, height - 60), footer_text, font=small_font, fill=footer_color)

#     out_path = os.path.join(base_dir, "static", "ad.png")
#     img.save(out_path)
#     return out_path
def generate_ad_image(
    header, para1, para2, subtext1, subtext2, footer,
    header_color, para1_color, para2_color, subtext_color,
    header_size, paragraph_size, subtext_size
):
    width, height = 1080, 1080
    img = Image.new("RGB", (width, height), color="#0070C0")  # blue background
    draw = ImageDraw.Draw(img)

    base_dir = os.path.dirname(__file__)
    font_path = os.path.join(base_dir, "static", "fonts", "Inter-Bold.ttf")

    try:
        header_font = ImageFont.truetype(font_path, size=header_size)
        paragraph_font = ImageFont.truetype(font_path, size=paragraph_size)
        subtext_font = ImageFont.truetype(font_path, size=subtext_size)
    except:
        header_font = paragraph_font = subtext_font = ImageFont.load_default()

    # --- Wrap and measure header + paragraphs ---
    y = 80
    content_width = width - 100

    header_lines = textwrap.wrap(header, width=30)
    para1_lines = textwrap.wrap(para1, width=35)
    para2_lines = textwrap.wrap(para2, width=40)

    # --- Draw Header (centered) ---
    for line in header_lines:
        bbox = draw.textbbox((0, 0), line, font=header_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, y), line, font=header_font, fill=header_color)
        y += bbox[3] - bbox[1] + 10

    y += 20

    # --- Estimate height for text block ---
    block_height = 0
    # for line in header_lines:
    #     bbox = draw.textbbox((0, 0), line, font=header_font)
    #     block_height += bbox[3] - bbox[1] + 10
    for line in para1_lines:
        bbox = draw.textbbox((0, 0), line, font=paragraph_font)
        block_height += bbox[3] - bbox[1] + 15
    for line in para2_lines:
        bbox = draw.textbbox((0, 0), line, font=paragraph_font)
        block_height += bbox[3] - bbox[1] + 15

    # --- Draw white rectangle box ---
    box_top = y - 10
    box_bottom = box_top + block_height + 180
    draw.rectangle([0, box_top, width, box_bottom], fill="white", outline="white", width=4)

    y += 20

    

    # --- Paragraph 1 ---
    for line in para1_lines:
        bbox = draw.textbbox((0, 0), line, font=paragraph_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, y), line, font=paragraph_font, fill=para1_color)
        y += bbox[3] - bbox[1] + 10

    y += 80

# --- Paragraph 2 ---
    for line in para2_lines:
        bbox = draw.textbbox((0, 0), line, font=paragraph_font)
        text_width = bbox[2] - bbox[0]
        draw.text(((width - text_width) / 2, y), line, font=paragraph_font, fill=para2_color)
        y += bbox[3] - bbox[1] + 10

    y = box_bottom + 50

    # --- Draw Logo (centered) ---
    logo_path = os.path.join(base_dir, "static", "images", "logo.png")
    try:
        logo = recolor_logo(logo_path, color="white")
        logo_width = 175
        logo_ratio = logo_width / logo.width
        logo_height = int(logo.height * logo_ratio)
        logo = logo.resize((logo_width, logo_height))
        img.paste(logo, ((width - logo_width) // 2, y), logo)
        y += logo_height + 30
    except Exception as e:
        print("Logo error:", e)

    # --- Subtext 1 ---
    for line in textwrap.wrap(subtext1, width=60):
        bbox = draw.textbbox((0, 0), line, font=subtext_font)
        draw.text(((width - bbox[2]) / 2, y), line, font=subtext_font, fill=subtext_color)
        y += bbox[3] - bbox[1] + 10

    y += 10

    # --- Subtext 2 ---
    for line in textwrap.wrap(subtext2, width=60):
        bbox = draw.textbbox((0, 0), line, font=subtext_font)
        draw.text(((width - bbox[2]) / 2, y), line, font=subtext_font, fill=subtext_color)
        y += bbox[3] - bbox[1] + 10

    # --- Footer ---
    y += 20
    bbox = draw.textbbox((0, 0), footer, font=header_font)
    draw.text(((width - bbox[2]) / 2, height - 60), footer, font=header_font, fill=header_color)

    # Save image
    output_path = os.path.join(base_dir, "static", "ad_output.png")
    img.save(output_path)
    return output_path
