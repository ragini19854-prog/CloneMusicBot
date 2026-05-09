import os
import re
import random
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from py_yt import VideosSearch

from MadaraMusic import app
from config import YOUTUBE_IMG_URL

FONT_BOLD = "assets/font_bold.ttf"
FONT_LIGHT = "assets/font_light.ttf"
TEMPLATE_PATH = "assets/bg_template.png"  # Use your new purple anime template
OUTPUT_DIR = "cache"

os.makedirs(OUTPUT_DIR, exist_ok=True)

async def download_image(url, path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                async with aiofiles.open(path, "wb") as f:
                    await f.write(await resp.read())
                return True
    return False

async def generate_thumbnail(videoid, title, duration, views, channel_name):
    thumb_path = os.path.join(OUTPUT_DIR, f"{videoid}.png")
    final_path = os.path.join(OUTPUT_DIR, f"final_{videoid}.png")

    # Download YT thumbnail
    yt_url = f"https://img.youtube.com/vi/{videoid}/maxresdefault.jpg"
    await download_image(yt_url, thumb_path)

    try:
        base = Image.open(TEMPLATE_PATH).convert("RGBA")
        cover = Image.open(thumb_path).convert("RGBA")
    except Exception as e:
        return f"Error: {e}"

    # Resize & paste cover (adjust position/size as per your template)
    cover = cover.resize((285, 160))
    base.paste(cover, (50, 520), cover)

    draw = ImageDraw.Draw(base)

    try:
        title_font = ImageFont.truetype(FONT_BOLD, 60)
        info_font = ImageFont.truetype(FONT_LIGHT, 30)
        brand_font = ImageFont.truetype(FONT_BOLD, 85)
    except:
        title_font = info_font = brand_font = ImageFont.load_default()

    # Text overlays (adjust coordinates for new design)
    draw.text((70, 180), channel_name, fill="white", font=brand_font)
    display_title = (title[:28] + "...") if len(title) > 28 else title
    draw.text((360, 545), display_title.upper(), fill="white", font=title_font)
    info_text = f"YouTube • {views} Views • {duration}"
    draw.text((360, 685), info_text, fill="#E0E0E0", font=info_font)

    # Progress bar
    draw.line([(50, 815), (1030, 815)], fill="#404040", width=8)
    draw.line([(50, 815), (520, 815)], fill="#FF00FF", width=8)  # Longer progress
    draw.ellipse([(510, 805), (530, 825)], fill="white")

    base.save(final_path)
    if os.path.exists(thumb_path):
        os.remove(thumb_path)

    return final_path
