import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

API_ID = int(getenv("API_ID", "0"))
API_HASH = getenv("API_HASH")

BOT_TOKEN = getenv("8693231254:AAFmLowrMpefZiS9XT8vfG3vUVPvuRu8E-E")
BOT_ID = getenv("8693231254)

OWNER_USERNAME = getenv("OWNER_USERNAME", "")
BOT_USERNAME = getenv("BOT_USERNAME", "")
BOT_NAME = getenv("BOT_NAME", "")
ASSUSERNAME = getenv("ASSUSERNAME", "")
BOT_LINK = getenv("BOT_LINK", "https://t.me/CLONNE_MUSIC_BOT?start=_tgr_QHn2CMQ5Njc1")

MONGO_DB_URI = getenv("mongodb+srv://bsdk:betichod@cluster0.fgj1r9z.mongodb.net/?retryWrites=true&w=majority")

YTPROXY_URL = getenv("YTPROXY_URL", 'https://tgapi.xbitcode.com')
YT_API_KEY = getenv("YT_API_KEY" , 'xbit_B4TNnBAoe6uoSM7NLFz-dk6X7GibJ6Bh')

DURATION_LIMIT_MIN = int(getenv("DURATION_LIMIT", 17000))

LOGGER_ID = int(getenv("LOGGER_ID", "0"))
CLONE_LOGGER = LOGGER_ID

OWNER_ID = int(getenv("OWNER_ID", "0"))

HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/ZXCVBNMASDFGHJKLQWERTYUIOP0786/SilentCloneBot",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv("GIT_TOKEN", "")

SUPPORT_CHANNEL = getenv("SUPPORT_CHANNEL", "https://t.me/Luckyxupdate")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "https://t.me/LuckyXSupport")
GITHUB = getenv("GITHUB", "https://t.me/LuckyXSupport")

AUTO_LEAVING_ASSISTANT = getenv("AUTO_LEAVING_ASSISTANT", "False")
AUTO_LEAVE_ASSISTANT_TIME = int(getenv("ASSISTANT_LEAVE_TIME", "9000"))

SONG_DOWNLOAD_DURATION = int(getenv("SONG_DOWNLOAD_DURATION", "9999999"))
SONG_DOWNLOAD_DURATION_LIMIT = int(getenv("SONG_DOWNLOAD_DURATION_LIMIT", "9999999"))

SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID", "1c21247d714244ddbb09925dac565aed")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET", "709e1a2969664491b58200860623ef19")

PLAYLIST_FETCH_LIMIT = int(getenv("PLAYLIST_FETCH_LIMIT", 25))
PLAYLIST_ID = -1001980154960

TG_AUDIO_FILESIZE_LIMIT = int(getenv("TG_AUDIO_FILESIZE_LIMIT", "5242880000"))
TG_VIDEO_FILESIZE_LIMIT = int(getenv("TG_VIDEO_FILESIZE_LIMIT", "5242880000"))

STRING1 = getenv("STRING_SESSION", "")
STRING2 = getenv("STRING_SESSION2", None)

BANNED_USERS = filters.user()
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}

START_IMG_URL = getenv("START_IMG_URL", "https://files.catbox.moe/37vii3.jpg").split()
HELP_IMG_URL = getenv("HELP_IMG_URL", "https://files.catbox.moe/u8ray8.jpg").split()
PING_IMG_URL = getenv("PING_IMG_URL", "https://files.catbox.moe/37vii3.jpg").split()

PLAYLIST_IMG_URL = getenv("PLAYLIST_IMG_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
STATS_IMG_URL = getenv("STATS_IMG_URL", "https://i.ibb.co/pBqPtFYn/statistics.jpg").split()
TELEGRAM_AUDIO_URL = getenv("TELEGRAM_AUDIO_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
TELEGRAM_VIDEO_URL = getenv("TELEGRAM_VIDEO_URL", "https://i.ibb.co/gL3ykkyh/play-music.jpg").split()
STREAM_IMG_URL = getenv("STREAM_IMG_URL", "https://i.ibb.co/0VKCS20y/stream.jpg").split()
SOUNCLOUD_IMG_URL = getenv("SOUNCLOUD_IMG_URL", "https://i.ibb.co/S4sPf3q8/soundcloud.jpg").split()
YOUTUBE_IMG_URL = getenv("YOUTUBE_IMG_URL", "https://i.ibb.co/xShkBVBK/youtube.jpg").split()
SPOTIFY_ARTIST_IMG_URL = getenv("SPOTIFY_ARTIST_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()
SPOTIFY_ALBUM_IMG_URL = getenv("SPOTIFY_ALBUM_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()
SPOTIFY_PLAYLIST_IMG_URL = getenv("SPOTIFY_PLAYLIST_IMG_URL", "https://i.ibb.co/XZfMS8Db/spotify.jpg").split()

def time_to_seconds(time):
    return sum(int(x) * 60**i for i, x in enumerate(reversed(str(time).split(":"))))

DURATION_LIMIT = int(time_to_seconds(f"{DURATION_LIMIT_MIN}:00"))

if SUPPORT_CHANNEL and not re.match("(?:http|https)://", SUPPORT_CHANNEL):
    raise SystemExit("[ERROR] - SUPPORT_CHANNEL url must start with https://")

if SUPPORT_CHAT and not re.match("(?:http|https)://", SUPPORT_CHAT):
    raise SystemExit("[ERROR] - SUPPORT_CHAT url must start with https://")

CMBOT = [
    "💞", "🥂", "🔍", "🧪", "⚡️", "🔥", "🦋", "🎩", "🌈", "🍷",
    "🥃", "🥤", "🕊️", "💌", "🧨", "✨", "💥", "💯", "🌟", "⚡️",
    "❤️", "😍", "🥰", "😘", "😂", "🤣", "😱", "😡", "👏", "🙏",
    "🎉", "🎊", "🎶", "🎵", "🎧", "🎸", "🎹", "🥁", "🎺", "🎷",
    "🔥", "⚡️", "💫", "🌙", "☀️", "🌈", "❄️", "🌸", "🌺", "🌹",
    "🦋", "🕊️", "🐍", "🐯", "🦁", "🐺", "🐉", "🦅", "🦄", "🐎"
]

EFFECT_ID = [
    5046509860389126442,
    5107584321108051014,
    5104841245755180586,
    5159385139981059251,
]
