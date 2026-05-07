import os
import re
import random
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode
from py_yt import VideosSearch
from PritiMusic import app
from config import YOUTUBE_IMG_URL
from PritiMusic.utils.database import clonebotdb 

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

def clear(text):
    list = text.split(" ")
    title = ""
    for i in list:
        if len(title) + len(i) < 60:
            title += " " + i
    return title.strip()

# ✅ Helper for Random Fallback Image
def get_random_fallback_img():
    if YOUTUBE_IMG_URL:
        if isinstance(YOUTUBE_IMG_URL, list):
            return random.choice(YOUTUBE_IMG_URL)
        return YOUTUBE_IMG_URL
    return "https://telegra.ph/file/2e3d368e77c449c287430.jpg"

async def get_thumb(videoid, user_id, client):
    # --- 1. Bot Name Fetch ---
    try:
        me = await client.get_me()
        bot_name = me.first_name.upper()
        bot_id = me.id
    except:
        bot_name = "MUSIC BOT"
        bot_id = 0

    # --- 2. Clone Owner Name Fetch ---
    owner_name = "OWNER" 
    try:
        bot_data = await clonebotdb.find_one({"bot_id": bot_id})
        if bot_data:
            owner_id = bot_data.get("user_id")
            try:
                owner = await client.get_users(owner_id)
                owner_name = owner.first_name.upper()
            except:
                owner_name = "UNKNOWN"
        else:
            owner_name = "MAIN BOT"
    except Exception as e:
        owner_name = "OWNER"

    # --- 3. Cache Check ---
    filename = f"cache/{videoid}_{bot_id}.png"
    if os.path.isfile(filename):
        return filename

    # --- 4. YouTube Thumbnail Download ---
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"

        async with aiohttp.ClientSession() as session:
            async with session.get(thumbnail) as resp:
                if resp.status == 200:
                    f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                    await f.write(await resp.read())
                    await f.close()

        youtube = Image.open(f"cache/thumb{videoid}.png")
        image1 = changeImageSize(1280, 720, youtube)
        image2 = image1.convert("RGBA")
        background = image2.filter(filter=ImageFilter.BoxBlur(10))
        enhancer = ImageEnhance.Brightness(background)
        background = enhancer.enhance(0.5)
        draw = ImageDraw.Draw(background)
        
        try:
            arial = ImageFont.truetype("PritiMusic/assets/font2.ttf", 30)
            font = ImageFont.truetype("PritiMusic/assets/font.ttf", 35)
        except:
            arial = ImageFont.load_default()
            font = ImageFont.load_default()

        # --- DRAWING TEXT ---

        # Right Side: BOT NAME
        try:
            try:
                bot_text_len = draw.textlength(f"{bot_name}   ", font=font)
            except:
                bot_text_len = 300 
            
            draw.text((1280 - int(bot_text_len) - 20, 20), f"{bot_name}", fill="yellow", font=font, stroke_width=1, stroke_fill="black")
        except:
            pass

        # Left Side: OWNER NAME
        try:
            draw.text((30, 20), f"OWNER: {owner_name}", fill="cyan", font=font, stroke_width=1, stroke_fill="black")
        except:
            pass

        # Song Info
        draw.text(
            (55, 560),
            f"{channel} | {views[:23]}",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (57, 600),
            clear(title),
            (255, 255, 255),
            font=font,
        )
        draw.line(
            [(55, 660), (1220, 660)],
            fill="white",
            width=5,
            joint="curve",
        )
        draw.ellipse(
            [(918, 648), (942, 672)],
            outline="white",
            fill="white",
            width=15,
        )
        draw.text(
            (36, 685),
            "00:00",
            (255, 255, 255),
            font=arial,
        )
        draw.text(
            (1185, 685),
            f"{duration[:23]}",
            (255, 255, 255),
            font=arial,
        )
        try:
            os.remove(f"cache/thumb{videoid}.png")
        except:
            pass
        
        background.save(filename)
        return filename

    except Exception as e:
        print(f"Thumb Error: {e}")
        # ✅ FIX: Return a single random URL string, not a List
        return get_random_fallback_img()