import asyncio
import glob
import json
import os
import random
import re
from typing import Union
import yt_dlp
import aiohttp
import aiofiles
from pyrogram.enums import MessageEntityType
from pyrogram.types import Message
from py_yt import VideosSearch
from PritiMusic import LOGGER
from PritiMusic.utils.formatters import time_to_seconds

YT_API_KEY = "xbit_R6rvFnM-f8VSANzscJRQT7VqMv_nxpfX"
YTPROXY = "https://tgapi.xbitcode.com"
FALLBACK_API_URL = "https://shrutibots.site"
YOUR_API_URL = None

CLIENT_SESSION = None

logger = LOGGER(__name__)

async def get_session():
    global CLIENT_SESSION
    if CLIENT_SESSION is None or CLIENT_SESSION.closed:
        connector = aiohttp.TCPConnector(limit=500, ttl_dns_cache=300)
        CLIENT_SESSION = aiohttp.ClientSession(connector=connector)
    return CLIENT_SESSION

async def load_api_url():
    global YOUR_API_URL
    try:
        session = await get_session()
        async with session.get("https://pastebin.com/raw/rLsBhAQa", timeout=5) as response:
            if response.status == 200:
                YOUR_API_URL = (await response.text()).strip()
            else:
                YOUR_API_URL = FALLBACK_API_URL
    except:
        YOUR_API_URL = FALLBACK_API_URL

try:
    loop = asyncio.get_event_loop()
    if loop.is_running():
        asyncio.create_task(load_api_url())
    else:
        loop.run_until_complete(load_api_url())
except RuntimeError:
    pass

def cookie_txt_file():
    try:
        folder = f"{os.getcwd()}/cookies"
        files = glob.glob(os.path.join(folder, '*.txt'))
        if not files: return None
        return f"cookies/{os.path.basename(random.choice(files))}"
    except:
        return None

async def check_file_size(link):
    async def get_format_info(link):
        proc = await asyncio.create_subprocess_exec(
            "yt-dlp", "--cookies", cookie_txt_file() or "", "-J", link,
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await proc.communicate()
        return json.loads(stdout.decode()) if proc.returncode == 0 else None

    info = await get_format_info(link)
    if not info: return None
    return sum(f.get('filesize', 0) for f in info.get('formats', []))

async def shell_cmd(cmd):
    proc = await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    out, err = await proc.communicate()
    return out.decode("utf-8") if out else err.decode("utf-8")

async def _download_stream(url, path, headers=None):
    try:
        session = await get_session()
        async with session.get(url, headers=headers, timeout=30) as response:
            if response.status != 200:
                return None
            
            async with aiofiles.open(path, mode='wb') as f:
                async for chunk in response.content.iter_chunked(524288): 
                    await f.write(chunk)
            return path
    except Exception:
        if os.path.exists(path):
            try: os.remove(path)
            except: pass
        return None

async def download_fallback_engine(link: str, is_video: bool) -> str:
    global YOUR_API_URL
    if not YOUR_API_URL: await load_api_url()

    vid_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link
    ext = "mp4" if is_video else "mp3"
    path = os.path.join("downloads", f"{vid_id}.{ext}")
    
    if os.path.exists(path): return path

    try:
        session = await get_session()
        v_type = "video" if is_video else "audio"
        
        async with session.get(f"{YOUR_API_URL}/download", params={"url": vid_id, "type": v_type}, timeout=8) as resp:
            if resp.status != 200: return None
            data = await resp.json()
            token = data.get("download_token")
            if not token: return None

        dl_url = f"{YOUR_API_URL}/stream/{vid_id}?type={v_type}"
        return await _download_stream(dl_url, path, headers={"X-Download-Token": token})
    except:
        return None

async def download_proxy_engine(vid_id: str, title: str, is_video: bool) -> str:
    ext = "mp4" if is_video else "mp3"
    fname = f"{title}.{ext}" if title else f"{vid_id}.{ext}"
    path = os.path.join("downloads", fname)
    
    if os.path.exists(path): return path

    try:
        session = await get_session()
        headers = {"x-api-key": YT_API_KEY}
        
        async with session.get(f"{YTPROXY}/info/{vid_id}", headers=headers, timeout=8) as resp:
            if resp.status != 200: return None
            data = await resp.json()
        
        if data.get('status') == 'success':
            url = data['video_url'] if is_video else data['audio_url']
            return await _download_stream(url, path)
        return None
    except:
        return None

class YouTubeAPI:
    def __init__(self):
        self.base = "https://www.youtube.com/watch?v="
        self.regex = r"(?:youtube\.com|youtu\.be)"
        self.listbase = "https://youtube.com/playlist?list="

    async def exists(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        return bool(re.search(self.regex, link))

    async def url(self, message_1: Message) -> Union[str, None]:
        messages = [message_1]
        if message_1.reply_to_message: messages.append(message_1.reply_to_message)
        for msg in messages:
            if msg.entities:
                for ent in msg.entities:
                    if ent.type == MessageEntityType.URL:
                        return (msg.text or msg.caption)[ent.offset : ent.offset + ent.length]
            elif msg.caption_entities:
                for ent in msg.caption_entities:
                    if ent.type == MessageEntityType.TEXT_LINK:
                        return ent.url
        return None

    async def details(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0]
        try:
            results = VideosSearch(link, limit=1)
            res = (await results.next())["result"][0]
            dur = res["duration"]
            return res["title"], dur, int(time_to_seconds(dur)) if dur else 0, res["thumbnails"][0]["url"].split("?")[0], res["id"]
        except:
            return None, "0", 0, None, None

    async def title(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        results = VideosSearch(link.split("&")[0], limit=1)
        return (await results.next())["result"][0]["title"]

    async def duration(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        results = VideosSearch(link.split("&")[0], limit=1)
        return (await results.next())["result"][0]["duration"]

    async def thumbnail(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        results = VideosSearch(link.split("&")[0], limit=1)
        return (await results.next())["result"][0]["thumbnails"][0]["url"].split("?")[0]

    async def video(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        fpath, _ = await self.download(link, None, video=True)
        return (1, fpath) if fpath else (0, "Failed")

    async def playlist(self, link, limit, user_id, videoid: Union[bool, str] = None):
        if videoid: link = self.listbase + link
        link = link.split("&")[0]
        cmd = f"yt-dlp -i --get-id --flat-playlist --cookies {cookie_txt_file()} --playlist-end {limit} --skip-download {link}"
        out = await shell_cmd(cmd)
        return [x for x in out.split("\n") if x]

    async def track(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0]
        res = (await VideosSearch(link, limit=1).next())["result"][0]
        return {
            "title": res["title"],
            "link": res["link"],
            "vidid": res["id"],
            "duration_min": res["duration"],
            "thumb": res["thumbnails"][0]["url"].split("?")[0],
        }, res["id"]

    async def formats(self, link: str, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0]
        ydl_opts = {"quiet": True, "cookiefile": cookie_txt_file()}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            formats = [
                {
                    "format": f["format"], "filesize": f.get("filesize"), 
                    "format_id": f["format_id"], "ext": f["ext"], 
                    "format_note": f.get("format_note"), "yturl": link
                } 
                for f in info["formats"] 
                if "dash" not in str(f.get("format", "")).lower() and f.get("filesize")
            ]
        return formats, link

    async def slider(self, link: str, query_type: int, videoid: Union[bool, str] = None):
        if videoid: link = self.base + link
        link = link.split("&")[0]
        results = (await VideosSearch(link, limit=10).next()).get("result", [])
        
        valid = []
        for res in results:
            try:
                t = time_to_seconds(res.get("duration", "0:00"))
                if t <= 3600: valid.append(res)
            except: pass
            
        if not valid or query_type >= len(valid): raise ValueError("No video")
        sel = valid[query_type]
        return sel["title"], sel["duration"], sel["thumbnails"][0]["url"].split("?")[0], sel["id"]

    async def download(
        self,
        link: str,
        mystic,
        video: Union[bool, str] = None,
        videoid: Union[bool, str] = None,
        songaudio: Union[bool, str] = None,
        songvideo: Union[bool, str] = None,
        format_id: Union[bool, str] = None,
        title: Union[bool, str] = None,
    ) -> str:
        if videoid:
            vid_id = link
            link = self.base + link
        else:
            vid_id = link.split('v=')[-1].split('&')[0] if 'v=' in link else link

        is_video = bool(video or songvideo)

        task1 = asyncio.create_task(download_fallback_engine(link, is_video))
        task2 = asyncio.create_task(download_proxy_engine(vid_id, title, is_video))
        
        pending = {task1, task2}

        while pending:
            done, pending = await asyncio.wait(pending, return_when=asyncio.FIRST_COMPLETED)
            
            for task in done:
                try:
                    result = await task
                    if result:
                        for p in pending: 
                            p.cancel()
                        return result, True
                except:
                    pass
        
        return None, False
