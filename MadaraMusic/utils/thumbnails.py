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

ASSETS = "MadaraMusic/assets"
THUMB_BG = os.path.join(ASSETS, "thumb_bg.png")
CACHE_DIR = "cache"

os.makedirs(CACHE_DIR, exist_ok=True)


def get_random_fallback_img():
    if YOUTUBE_IMG_URL:
        if isinstance(YOUTUBE_IMG_URL, list):
            return random.choice(YOUTUBE_IMG_URL)
        return YOUTUBE_IMG_URL
    return "https://telegra.ph/file/2e3d368e77c449c287430.jpg"


def _load_font(name, size):
    path = os.path.join(ASSETS, name)
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def _truncate(text, max_chars):
    return (text[:max_chars] + "...") if len(text) > max_chars else text


def _draw_rounded_rect(draw, xy, radius, fill):
    x1, y1, x2, y2 = xy
    draw.rectangle([x1 + radius, y1, x2 - radius, y2], fill=fill)
    draw.rectangle([x1, y1 + radius, x2, y2 - radius], fill=fill)
    draw.ellipse([x1, y1, x1 + radius * 2, y1 + radius * 2], fill=fill)
    draw.ellipse([x2 - radius * 2, y1, x2, y1 + radius * 2], fill=fill)
    draw.ellipse([x1, y2 - radius * 2, x1 + radius * 2, y2], fill=fill)
    draw.ellipse([x2 - radius * 2, y2 - radius * 2, x2, y2], fill=fill)


async def get_thumb(videoid):
    out_path = os.path.join(CACHE_DIR, f"{videoid}.png")
    if os.path.isfile(out_path):
        return out_path

    url = f"https://www.youtube.com/watch?v={videoid}"
    title = "Unknown Title"
    duration = "0:00"
    views = "0"
    channel = "Unknown"
    thumbnail_url = None

    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub(r"\W+", " ", title).strip().title()
            except Exception:
                pass
            try:
                duration = result["duration"] or "0:00"
            except Exception:
                pass
            try:
                thumbnail_url = result["thumbnails"][0]["url"].split("?")[0]
            except Exception:
                pass
            try:
                views = result["viewCount"]["short"]
            except Exception:
                pass
            try:
                channel = result["channel"]["name"]
            except Exception:
                pass
    except Exception as e:
        print(f"[Thumbnail] Search error: {e}")
        return get_random_fallback_img()

    # Download the YouTube cover thumbnail
    cover_path = os.path.join(CACHE_DIR, f"cover_{videoid}.png")
    cover_ok = False
    if thumbnail_url:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail_url) as resp:
                    if resp.status == 200:
                        async with aiofiles.open(cover_path, "wb") as f:
                            await f.write(await resp.read())
                        cover_ok = True
        except Exception as e:
            print(f"[Thumbnail] Cover download error: {e}")

    try:
        # --- Load background template ---
        bg = Image.open(THUMB_BG).convert("RGBA")
        W, H = bg.size  # 1536 x 1024

        draw = ImageDraw.Draw(bg, "RGBA")

        # --- Paste small album cover (lower-left box) ---
        # Approx position of the small thumbnail slot in the image
        COVER_X, COVER_Y = 75, 655
        COVER_W, COVER_H = 368, 207

        if cover_ok and os.path.isfile(cover_path):
            try:
                cover_img = Image.open(cover_path).convert("RGBA")
                cover_img = cover_img.resize((COVER_W, COVER_H), Image.LANCZOS)
                bg.paste(cover_img, (COVER_X, COVER_Y), cover_img)
            except Exception as e:
                print(f"[Thumbnail] Cover paste error: {e}")

        # --- Fonts ---
        font_title = _load_font("font2.ttf", 68)
        font_info  = _load_font("semibold.ttf", 36)
        font_badge = _load_font("font.ttf", 30)
        font_time  = _load_font("semibold.ttf", 38)

        # --- Song title (upper-case, white, in the middle-right area) ---
        title_text = _truncate(title.upper(), 22)
        draw.text((468, 658), title_text, fill="white", font=font_title)

        # --- "Full Video" and "4K" badges ---
        _draw_rounded_rect(draw, (468, 748, 590, 790), 8, (255, 255, 255, 40))
        draw.text((480, 752), "Full Video", fill="white", font=font_badge)

        _draw_rounded_rect(draw, (604, 748, 660, 790), 8, (255, 200, 0, 60))
        draw.text((614, 752), "4K", fill=(255, 220, 0), font=font_badge)

        # --- Channel · Views · Duration info row ---
        info_text = f"YouTube  •  {views}  •  {duration}"
        draw.text((468, 800), info_text, fill="#cccccc", font=font_info)

        # --- Progress bar ---
        BAR_X1, BAR_Y = 75, 900
        BAR_X2 = W - 180
        BAR_H = 7

        # Background track
        _draw_rounded_rect(draw, (BAR_X1, BAR_Y - BAR_H // 2, BAR_X2, BAR_Y + BAR_H // 2), 4, (80, 80, 80, 200))

        # Filled portion (~25% through)
        progress_x = BAR_X1 + int((BAR_X2 - BAR_X1) * 0.25)
        _draw_rounded_rect(draw, (BAR_X1, BAR_Y - BAR_H // 2, progress_x, BAR_Y + BAR_H // 2), 4, (255, 0, 255, 220))

        # Scrubber circle
        draw.ellipse(
            (progress_x - 14, BAR_Y - 14, progress_x + 14, BAR_Y + 14),
            fill="white"
        )

        # --- Time stamps ---
        draw.text((BAR_X1, BAR_Y + 20), "00:25", fill="white", font=font_time)
        dur_text = _truncate(duration, 10)
        try:
            bb = draw.textbbox((0, 0), dur_text, font=font_time)
            dur_w = bb[2] - bb[0]
        except Exception:
            dur_w = 80
        draw.text((BAR_X2 - dur_w, BAR_Y + 20), dur_text, fill="white", font=font_time)

        # --- Save ---
        final = bg.convert("RGB")
        final.save(out_path)

    except Exception as e:
        print(f"[Thumbnail] Render error: {e}")
        return get_random_fallback_img()
    finally:
        try:
            os.remove(cover_path)
        except Exception:
            pass

    return out_path
