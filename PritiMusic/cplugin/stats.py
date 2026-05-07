import platform
import random
from sys import version as pyver

import psutil
from pyrogram import __version__ as pyrover
from pyrogram import filters, Client
from pyrogram.errors import MessageIdInvalid
from pyrogram.types import InputMediaPhoto, Message
from pytgcalls.__version__ import __version__ as pytgver

import config
from PritiMusic import app
from PritiMusic.core.userbot import assistants
from PritiMusic.misc import SUDOERS, mongodb
from PritiMusic.plugins import ALL_MODULES
from PritiMusic.utils.database import (
    get_served_chats_clone,
    get_served_users_clone,
    get_sudoers,
)
from PritiMusic.utils.decorators.language import language, languageCB
from PritiMusic.utils.inline.stats import back_stats_buttons, stats_buttons
from config import BANNED_USERS


# ✅ Helper to get Random Stats Image
def get_random_stats_img():
    if config.STATS_IMG_URL:
        if isinstance(config.STATS_IMG_URL, list):
            return random.choice(config.STATS_IMG_URL)
        return config.STATS_IMG_URL
    return "https://telegra.ph/file/2e3d368e77c449c287430.jpg" # Fallback


@Client.on_message(filters.command(["stats", "gstats"]) & ~BANNED_USERS)
@language
async def stats_global(client: Client, message: Message, _):
    a = await client.get_me()
    bot_id = a.id

    upl = stats_buttons(_, True if message.from_user.id in SUDOERS else False)
    
    # ✅ Random Image + Spoiler
    await message.reply_photo(
        photo=get_random_stats_img(),
        caption=_["gstats_2"].format(a.mention),
        reply_markup=upl,
        has_spoiler=True
    )


@Client.on_callback_query(filters.regex("stats_back") & ~BANNED_USERS)
@languageCB
async def home_stats(client, CallbackQuery, _):
    a = await client.get_me()
    bot_id = a.id
    upl = stats_buttons(_, True if CallbackQuery.from_user.id in SUDOERS else False)
    
    # Back button typically edits text. If you want to change media, use edit_message_media.
    await CallbackQuery.edit_message_text(
        text=_["gstats_2"].format(a.mention),
        reply_markup=upl,
    )


@Client.on_callback_query(filters.regex("TopOverall") & ~BANNED_USERS)
@languageCB
async def overall_stats(client, CallbackQuery, _):
    a = await client.get_me()
    bot_id = a.id
    try:
        await CallbackQuery.answer()
    except:
        pass
    upl = back_stats_buttons(_)
    
    # Edit text to show loading...
    await CallbackQuery.edit_message_text(_["gstats_1"].format(a.mention))
    
    # Fetch Clone Stats
    served_chats = len(await get_served_chats_clone(bot_id))
    served_users = len(await get_served_users_clone(bot_id))
    
    text = _["gstats_3"].format(
        a.mention,
        len(assistants),
        len(BANNED_USERS),
        served_chats,
        served_users,
        len(ALL_MODULES),
        len(SUDOERS),
        config.AUTO_LEAVING_ASSISTANT,
        config.DURATION_LIMIT_MIN,
    )
    
    # ✅ Random Image + Spoiler for Media Edit
    med = InputMediaPhoto(media=get_random_stats_img(), caption=text, has_spoiler=True)
    
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=get_random_stats_img(), caption=text, reply_markup=upl, has_spoiler=True
        )


@Client.on_callback_query(filters.regex("bot_stats_sudo"))
@languageCB
async def bot_stats(client, CallbackQuery, _):
    a = await client.get_me()
    bot_id = a.id
    if CallbackQuery.from_user.id not in SUDOERS:
        return await CallbackQuery.answer(_["gstats_4"], show_alert=True)
    upl = back_stats_buttons(_)
    try:
        await CallbackQuery.answer()
    except:
        pass
        
    await CallbackQuery.edit_message_text(_["gstats_1"].format(a.mention))
    
    p_core = psutil.cpu_count(logical=False)
    t_core = psutil.cpu_count(logical=True)
    ram = str(round(psutil.virtual_memory().total / (1024.0**3))) + " GB"
    try:
        cpu_freq = psutil.cpu_freq().current
        if cpu_freq >= 1000:
            cpu_freq = f"{round(cpu_freq / 1000, 2)}GHz"
        else:
            cpu_freq = f"{round(cpu_freq, 2)}MHz"
    except:
        cpu_freq = "Failed to fetch"
    
    hdd = psutil.disk_usage("/")
    total = hdd.total / (1024.0**3)
    used = hdd.used / (1024.0**3)
    free = hdd.free / (1024.0**3)
    call = await mongodb.command("dbstats")
    datasize = call["dataSize"] / 1024
    storage = call["storageSize"] / 1024
    
    # Fetch Clone Stats
    served_chats = len(await get_served_chats_clone(bot_id))
    served_users = len(await get_served_users_clone(bot_id))
    
    text = _["gstats_5"].format(
        a.mention,
        len(ALL_MODULES),
        platform.system(),
        ram,
        p_core,
        t_core,
        cpu_freq,
        pyver.split()[0],
        pyrover,
        pytgver,
        str(total)[:4],
        str(used)[:4],
        str(free)[:4],
        served_chats,
        served_users,
        len(BANNED_USERS),
        len(await get_sudoers()),
        str(datasize)[:6],
        storage,
        call["collections"],
        call["objects"],
    )
    
    # ✅ Random Image + Spoiler for Media Edit
    med = InputMediaPhoto(media=get_random_stats_img(), caption=text, has_spoiler=True)
    
    try:
        await CallbackQuery.edit_message_media(media=med, reply_markup=upl)
    except MessageIdInvalid:
        await CallbackQuery.message.reply_photo(
            photo=get_random_stats_img(), caption=text, reply_markup=upl, has_spoiler=True
        )