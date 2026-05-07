import random
import string
import asyncio
from random import randint
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InputMediaPhoto, Message, InlineKeyboardButton
from pytgcalls.exceptions import NoActiveGroupCall
from PritiMusic.utils.database import get_assistant
import config
from PritiMusic import Apple, Resso, SoundCloud, Spotify, Telegram, YouTube, app
from PritiMusic.core.call import Lucky
from PritiMusic.misc import SUDOERS, db

# ✅ IMPORT: Ab 'buttons.py' se import ho raha hai
from PritiMusic.cplugin.buttons import (
    livestream_markup,
    playlist_markup,
    slider_markup,
    track_markup,
    queue_markup,
    stream_markup,
    stream_markup2,
    panel_markup_1,
    panel_markup_2,
    panel_markup_3,
    panel_markup_4,
    panel_markup_5,
    panel_markup_clone,
    telegram_markup
)

from PritiMusic.utils import seconds_to_min, time_to_seconds
from PritiMusic.utils.channelplay import get_channeplayCB
from PritiMusic.utils.decorators.language import languageCB
from PritiMusic.utils.decorators.play import CPlayWrapper
from PritiMusic.utils.formatters import formats
from PritiMusic.utils.inline import close_markup, aq_markup

from PritiMusic.utils.database import (
    add_served_user_clone,
    is_active_chat,
    add_active_video_chat,
    clonebotdb
)

from PritiMusic.utils.database.clonedb import (
    get_owner_id_from_db, 
    get_cloned_support_chat, 
    get_clone_search_settings,
    get_clone_stream_caption
)

from PritiMusic.utils.exceptions import AssistantErr
from PritiMusic.utils.pastebin import LuckyBin
from PritiMusic.utils.stream.queue import put_queue, put_queue_index
from PritiMusic.utils.logger import play_logs, clone_bot_logs
from PritiMusic.cplugin.setinfo import get_logging_status, get_log_channel
from PritiMusic.cplugin.utils.cthumbnail import get_thumb

from config import BANNED_USERS, lyrical
from time import time
from datetime import datetime
from typing import Union

user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

def get_random_img(img_list):
    if img_list:
        if isinstance(img_list, list):
            return random.choice(img_list)
        return img_list
    return "https://telegra.ph/file/2e3d368e77c449c287430.jpg"

@Client.on_message(
    filters.command(
        [
            "play", "vplay", "cplay", "cvplay", "playforce", "vplayforce", "cplayforce", "cvplayforce"
        ],
        prefixes=["/", "!", "%", "", ".", "@", "#"],
    )
    & filters.group
    & ~BANNED_USERS
)
@CPlayWrapper
async def play_commnd(client, message: Message, _, chat_id, video, channel, playmode, url, fplay):
    cuser = await client.get_me()
    try:
        if cuser.username:
            await clonebotdb.update_one(
                {"username": cuser.username},
                {"$set": {"last_activity": datetime.now()}}
            )
    except Exception:
        pass

    bot_id = cuser.id
    user_id = message.from_user.id

    if hasattr(client, "assistant") and client.assistant:
        userbot = client.assistant
    else:
        userbot = await get_assistant(chat_id)

    C_BOT_OWNER_ID = await get_owner_id_from_db(bot_id)
    bot_mention = cuser.mention
    
    try:
        C_LOG_STATUS = await get_logging_status(bot_id)
        C_LOGGER_ID = await get_log_channel(bot_id)
    except:
        C_LOG_STATUS = True 
        C_LOGGER_ID = config.CLONE_LOGGER

    if str(C_LOGGER_ID) == "-100":
        C_LOGGER_ID = C_BOT_OWNER_ID

    clone_logger_id = C_LOGGER_ID

    current_time = time()
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            hu = await message.reply_text(f"**{message.from_user.mention} Please do not spam. Try again in 5 seconds.**")
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    await add_served_user_clone(message.chat.id, bot_id)
    
    try:
        stype, scontent = await get_clone_search_settings(bot_id)
        if stype == "text" and scontent:
            mystic = await message.reply_text(scontent)
        elif stype == "sticker" and scontent:
            mystic = await message.reply_sticker(scontent)
        elif stype == "animation" and scontent:
            mystic = await message.reply_animation(scontent)
        elif stype == "video" and scontent:
            mystic = await message.reply_video(scontent)
        elif stype == "photo" and scontent:
            mystic = await message.reply_photo(scontent)
        else:
            mystic = await message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])
    except Exception as e:
        mystic = await message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])

    plist_id = None
    slider = None
    plist_type = None
    spotify = None
    user_id = message.from_user.id
    user_name = message.from_user.mention

    audio_telegram = ((message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None)
    video_telegram = ((message.reply_to_message.video or message.reply_to_message.document) if message.reply_to_message else None)
    
    if audio_telegram:
        if audio_telegram.file_size > 104857600:
            return await mystic.edit_text(_["play_5"])
        duration_min = seconds_to_min(audio_telegram.duration)
        if (audio_telegram.duration) > config.DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, cuser.mention))
        file_path = await Telegram.get_filepath(audio=audio_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(audio_telegram, audio=True)
            dur = await Telegram.get_duration(audio_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                await stream(client, _, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="telegram", forceplay=fplay, userbot=userbot)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                print(e)
                return await mystic.edit_text(e)
            return await mystic.delete()
        return
    elif video_telegram:
        if message.reply_to_message.document:
            try:
                ext = video_telegram.file_name.split(".")[-1]
                if ext.lower() not in formats:
                    return await mystic.edit_text(_["play_7"].format(f"{' | '.join(formats)}"))
            except:
                return await mystic.edit_text(_["play_7"].format(f"{' | '.join(formats)}"))
        if video_telegram.file_size > config.TG_VIDEO_FILESIZE_LIMIT:
            return await mystic.edit_text(_["play_8"])
        file_path = await Telegram.get_filepath(video=video_telegram)
        if await Telegram.download(_, message, mystic, file_path):
            message_link = await Telegram.get_link(message)
            file_name = await Telegram.get_filename(video_telegram)
            dur = await Telegram.get_duration(video_telegram, file_path)
            details = {"title": file_name, "link": message_link, "path": file_path, "dur": dur}
            try:
                await stream(client, _, mystic, user_id, details, chat_id, user_name, message.chat.id, video=True, streamtype="telegram", forceplay=fplay, userbot=userbot)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                print(e)
                return await mystic.edit_text(e)
            return await mystic.delete()
        return
    elif url:
        if not url.startswith(("http://", "https://")):
            return await mystic.edit_text("❌ **Security Error:** Local files are not allowed.")
        allowed_domains = ["youtube.com", "youtu.be", "spotify.com", "soundcloud.com", "m.soundcloud.com", "music.apple.com", "resso.com"]
        if not any(domain in url for domain in allowed_domains):
             return await mystic.edit_text("❌ **Unsupported Link!**")
        if await YouTube.exists(url):
            if "playlist" in url:
                try:
                    details = await YouTube.playlist(url, config.PLAYLIST_FETCH_LIMIT, message.from_user.id)
                except Exception as e:
                    print(e)
                    return await mystic.edit_text("❌ Failed to fetch playlist.")
                streamtype = "playlist"
                plist_type = "yt"
                if "&" in url:
                    plist_id = (url.split("=")[1]).split("&")[0]
                else:
                    plist_id = url.split("=")[1]
                img = get_random_img(config.PLAYLIST_IMG_URL)
                cap = _["play_10"]
            elif "https://youtu.be" in url:
                videoid = url.split("/")[-1].split("?")[0]
                details, track_id = await YouTube.track(f"https://www.youtube.com/watch?v={videoid}")
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
            else:
                try:
                    details, track_id = await YouTube.track(url)
                except Exception as e:
                    print(e)
                    return await mystic.edit_text("❌ Error fetching YouTube track.")
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_11"].format(details["title"], details["duration_min"])
        elif await Spotify.valid(url):
            spotify = True
            if not config.SPOTIFY_CLIENT_ID and not config.SPOTIFY_CLIENT_SECRET:
                return await mystic.edit_text("» Spotify is not supported yet.")
            if "track" in url:
                try:
                    details, track_id = await Spotify.track(url)
                except:
                    return await mystic.edit_text("❌ Error fetching Spotify track.")
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                try:
                    details, plist_id = await Spotify.playlist(url)
                except Exception:
                    return await mystic.edit_text("❌ Error fetching Spotify playlist.")
                streamtype = "playlist"
                plist_type = "spplay"
                img = get_random_img(config.SPOTIFY_PLAYLIST_IMG_URL)
                cap = _["play_11"].format(cuser.mention, message.from_user.mention)
            elif "album" in url:
                try:
                    details, plist_id = await Spotify.album(url)
                except:
                    return await mystic.edit_text("❌ Error fetching Spotify album.")
                streamtype = "playlist"
                plist_type = "spalbum"
                img = get_random_img(config.SPOTIFY_ALBUM_IMG_URL)
                cap = _["play_11"].format(cuser.mention, message.from_user.mention)
            elif "artist" in url:
                try:
                    details, plist_id = await Spotify.artist(url)
                except:
                    return await mystic.edit_text("❌ Error fetching Spotify artist.")
                streamtype = "playlist"
                plist_type = "spartist"
                img = get_random_img(config.SPOTIFY_ARTIST_IMG_URL)
                cap = _["play_11"].format(message.from_user.first_name)
            else:
                return await mystic.edit_text(_["play_15"])
        elif await Apple.valid(url):
            if "album" in url:
                try:
                    details, track_id = await Apple.track(url)
                except:
                    return await mystic.edit_text("❌ Error fetching Apple track.")
                streamtype = "youtube"
                img = details["thumb"]
                cap = _["play_10"].format(details["title"], details["duration_min"])
            elif "playlist" in url:
                spotify = True
                try:
                    details, plist_id = await Apple.playlist(url)
                except:
                    return await mystic.edit_text("❌ Error fetching Apple playlist.")
                streamtype = "playlist"
                plist_type = "apple"
                cap = _["play_12"].format(cuser.mention, message.from_user.mention)
                img = url
            else:
                return await mystic.edit_text("❌ Error: Invalid Apple Music link.")
        elif await Resso.valid(url):
            try:
                details, track_id = await Resso.track(url)
            except:
                return await mystic.edit_text("❌ Error fetching Resso track.")
            streamtype = "youtube"
            img = details["thumb"]
            cap = _["play_10"].format(details["title"], details["duration_min"])
        elif await SoundCloud.valid(url):
            try:
                details, track_path = await SoundCloud.download(url)
            except:
                return await mystic.edit_text("❌ Error fetching SoundCloud track.")
            duration_sec = details["duration_sec"]
            if duration_sec > config.DURATION_LIMIT:
                return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, cuser.mention))
            try:
                await stream(client, _, mystic, user_id, details, chat_id, user_name, message.chat.id, streamtype="soundcloud", forceplay=fplay, userbot=userbot)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                print(e)
                return await mystic.edit_text(e)
            return await mystic.delete()
        else:
            try:
                await Lucky.stream_call(url)
            except NoActiveGroupCall:
                await mystic.edit_text(_["black_9"])
                return await app.send_message(chat_id=config.CLONE_LOGGER, text=_["play_17"])
            except Exception as e:
                if "phone.CreateGroupCall" in str(e):
                    await mystic.edit_text(_["black_9"])
                    return await app.send_message(chat_id=config.CLONE_LOGGER, text=_["play_17"])
                else:
                    print(e)
                    return await mystic.edit_text(_["general_2"].format(type(e).__name__))
            await mystic.edit_text(_["str_2"])
            try:
                await stream(client, _, mystic, message.from_user.id, url, chat_id, message.from_user.first_name, message.chat.id, video=video, streamtype="index", forceplay=fplay, userbot=userbot)
            except Exception as e:
                ex_type = type(e).__name__
                err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
                print(e)
                return await mystic.edit_text(e)
            if C_LOG_STATUS:
                try:
                    await clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype="M3u8 or Index Link")
                except Exception as e:
                    print(f"[ERROR] Failed to send logging enabled message: {e}")
            return await play_logs(message, streamtype="M3u8 or Index Link")
    else:
        if len(message.command) < 2:
            try:
                a = await client.get_me()
                C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(a.id)
                if C_BOT_SUPPORT_CHAT:
                    C_SUPPORT_CHAT = C_BOT_SUPPORT_CHAT if "https://" in C_BOT_SUPPORT_CHAT else f"https://t.me/{C_BOT_SUPPORT_CHAT}"
                else:
                    C_SUPPORT_CHAT = config.SUPPORT_CHAT
            except:
                C_SUPPORT_CHAT = config.SUPPORT_CHAT
            buttons = InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Support", url=C_SUPPORT_CHAT), InlineKeyboardButton(text="Close", callback_data="close")]]
            )
            play_img = get_random_img(config.PLAYLIST_IMG_URL)
            try:
                stype, scontent = await get_clone_search_settings(bot_id)
                if stype == "photo" and scontent:
                     play_img = scontent
            except:
                pass
            await mystic.delete()
            return await message.reply_photo(photo=play_img, caption=_["play_18"], reply_markup=buttons, has_spoiler=True)
        slider = True
        query = message.text.split(None, 1)[1]
        if "-v" in query:
            query = query.replace("-v", "")
        try:
            details, track_id = await YouTube.track(query)
        except:
            return await mystic.edit_text("❌ Error searching on YouTube.")
        streamtype = "youtube"
    if str(playmode) == "Direct":
        if not plist_type:
            if details["duration_min"]:
                duration_sec = time_to_seconds(details["duration_min"])
                if duration_sec > config.DURATION_LIMIT:
                    return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, cuser.mention))
            else:
                buttons = livestream_markup(_, track_id, user_id, "v" if video else "a", "c" if channel else "g", "f" if fplay else "d")
                return await mystic.edit_text(_["play_13"], reply_markup=InlineKeyboardMarkup(buttons))
        try:
            await stream(client, _, mystic, user_id, details, chat_id, user_name, message.chat.id, video=video, streamtype=streamtype, spotify=spotify, forceplay=fplay, userbot=userbot)
        except Exception as e:
            ex_type = type(e).__name__
            err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
            print(e)
            return await mystic.edit_text(e)
        await mystic.delete()
        if C_LOG_STATUS:
            try:
                await clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype=streamtype)
            except Exception as e:
                print(f"[ERROR] Failed to send logging enabled message: {e}")
        return await play_logs(message, streamtype=streamtype)
    else:
        if plist_type:
            ran_hash = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
            lyrical[ran_hash] = plist_id
            buttons = playlist_markup(_, ran_hash, message.from_user.id, plist_type, "c" if channel else "g", "f" if fplay else "d")
            await mystic.delete()
            await message.reply_photo(photo=img, caption=cap, reply_markup=InlineKeyboardMarkup(buttons), has_spoiler=True)
            if C_LOG_STATUS:
                try:
                    await clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype=f"Playlist : {plist_type}")
                except Exception as e:
                    print(f"[ERROR] Failed to send logging enabled message: {e}")
            return await play_logs(message, streamtype=f"Playlist : {plist_type}")
        else:
            if slider:
                buttons = slider_markup(_, track_id, message.from_user.id, query, 0, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                await message.reply_photo(photo=details["thumb"], caption=_["play_10"].format(details["title"].title(), details["duration_min"]), reply_markup=InlineKeyboardMarkup(buttons), has_spoiler=True)
                if C_LOG_STATUS:
                    try:
                        await clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype=f"Searched on Youtube")
                    except Exception as e:
                        print(f"[ERROR] Failed to send logging enabled message: {e}")
                return await play_logs(message, streamtype=f"Searched on Youtube")
            else:
                buttons = track_markup(_, track_id, message.from_user.id, "c" if channel else "g", "f" if fplay else "d")
                await mystic.delete()
                await message.reply_photo(photo=img, caption=cap, reply_markup=InlineKeyboardMarkup(buttons), has_spoiler=True)
                if C_LOG_STATUS:
                    try:
                        await clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype=f"URL Searched Inline")
                    except Exception as e:
                        print(f"[ERROR] Failed to send logging enabled message: {e}")
                return await play_logs(message, streamtype=f"URL Searched Inline")

@Client.on_callback_query(filters.regex("MusicStream") & ~BANNED_USERS)
@languageCB
async def play_music(client: Client, CallbackQuery, _):
    cuser = await client.get_me()
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    vidid, user_id, mode, cplay, fplay = callback_request.split("|")
    if hasattr(client, "assistant") and client.assistant:
        userbot = client.assistant
    else:
        try:
            chat_id, _ = await get_channeplayCB(_, cplay, CallbackQuery)
            userbot = await get_assistant(chat_id)
        except:
            userbot = await get_assistant(CallbackQuery.message.chat.id)
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return
    user_name = CallbackQuery.from_user.mention
    try:
        await CallbackQuery.message.delete()
        await CallbackQuery.answer()
    except:
        pass
    bot_id = client.me.id
    try:
        stype, scontent = await get_clone_search_settings(bot_id)
        if stype == "sticker":
            mystic = await CallbackQuery.message.reply_sticker(scontent)
        elif stype == "animation":
            mystic = await CallbackQuery.message.reply_animation(scontent)
        elif stype == "text" and scontent:
            mystic = await CallbackQuery.message.reply_text(scontent)
        elif stype == "video" and scontent:
             mystic = await CallbackQuery.message.reply_video(scontent)
        elif stype == "photo" and scontent:
             mystic = await CallbackQuery.message.reply_photo(scontent)
        else:
            mystic = await CallbackQuery.message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])
    except:
        mystic = await CallbackQuery.message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])
    try:
        details, track_id = await YouTube.track(vidid, True)
    except:
        return await mystic.edit_text("❌ Error processing request.")
    if details["duration_min"]:
        duration_sec = time_to_seconds(details["duration_min"])
        if duration_sec > config.DURATION_LIMIT:
            return await mystic.edit_text(_["play_6"].format(config.DURATION_LIMIT_MIN, cuser.mention))
    else:
        buttons = livestream_markup(_, track_id, CallbackQuery.from_user.id, mode, "c" if cplay == "c" else "g", "f" if fplay else "d")
        return await mystic.edit_text(_["play_13"], reply_markup=InlineKeyboardMarkup(buttons))
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    try:
        await stream(client, _, mystic, CallbackQuery.from_user.id, details, chat_id, user_name, CallbackQuery.message.chat.id, video, streamtype="youtube", forceplay=ffplay, userbot=userbot)
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
        print(e)
        return await mystic.edit_text(e)
    return await mystic.delete()

@Client.on_callback_query(filters.regex("ZEOmousAdmin") & ~BANNED_USERS)
async def ZEOmous_check(client: Client, CallbackQuery):
    try:
        await CallbackQuery.answer("Revert back to user account:\n\nOpen group settings.\n-> Administrators\n-> Click on your name\n-> Uncheck anonymous admin permissions.", show_alert=True)
    except:
        pass

@Client.on_callback_query(filters.regex("ZEOPlaylists") & ~BANNED_USERS)
@languageCB
async def play_playlists_command(client: Client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (videoid, user_id, ptype, mode, cplay, fplay) = callback_request.split("|")
    if hasattr(client, "assistant") and client.assistant:
        userbot = client.assistant
    else:
        try:
            chat_id, _ = await get_channeplayCB(_, cplay, CallbackQuery)
            userbot = await get_assistant(chat_id)
        except:
            userbot = await get_assistant(CallbackQuery.message.chat.id)
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except:
            return
    try:
        chat_id, channel = await get_channeplayCB(_, cplay, CallbackQuery)
    except:
        return
    user_name = CallbackQuery.from_user.mention
    await CallbackQuery.message.delete()
    try:
        await CallbackQuery.answer()
    except:
        pass
    bot_id = client.me.id
    try:
        stype, scontent = await get_clone_search_settings(bot_id)
        if stype == "sticker":
            mystic = await CallbackQuery.message.reply_sticker(scontent)
        elif stype == "animation":
            mystic = await CallbackQuery.message.reply_animation(scontent)
        elif stype == "text" and scontent:
            mystic = await CallbackQuery.message.reply_text(scontent)
        elif stype == "video" and scontent:
             mystic = await CallbackQuery.message.reply_video(scontent)
        elif stype == "photo" and scontent:
             mystic = await CallbackQuery.message.reply_photo(scontent)
        else:
            mystic = await CallbackQuery.message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])
    except:
        mystic = await CallbackQuery.message.reply_text(_["play_2"].format(channel) if channel else _["play_1"])
    videoid = lyrical.get(videoid)
    video = True if mode == "v" else None
    ffplay = True if fplay == "f" else None
    spotify = True
    if ptype == "yt":
        spotify = False
        try:
            result = await YouTube.playlist(videoid, config.PLAYLIST_FETCH_LIMIT, CallbackQuery.from_user.id, True)
        except:
            return await mystic.edit_text("❌ Error fetching playlist.")
    if ptype == "spplay":
        try:
            result, spotify_id = await Spotify.playlist(videoid)
        except:
            return await mystic.edit_text("❌ Error fetching Spotify playlist.")
    if ptype == "spalbum":
        try:
            result, spotify_id = await Spotify.album(videoid)
        except:
            return await mystic.edit_text("❌ Error fetching Spotify album.")
    if ptype == "spartist":
        try:
            result, spotify_id = await Spotify.artist(videoid)
        except:
            return await mystic.edit_text("❌ Error fetching Spotify artist.")
    if ptype == "apple":
        try:
            result, apple_id = await Apple.playlist(videoid, True)
        except:
            return await mystic.edit_text("❌ Error fetching Apple playlist.")
    try:
        await stream(client, _, mystic, user_id, result, chat_id, user_name, CallbackQuery.message.chat.id, video, streamtype="playlist", spotify=spotify, forceplay=ffplay, userbot=userbot)
    except Exception as e:
        ex_type = type(e).__name__
        err = e if ex_type == "AssistantErr" else _["general_2"].format(ex_type)
        print(e)
        return await mystic.edit_text(e)
    return await mystic.delete()

@Client.on_callback_query(filters.regex("slider") & ~BANNED_USERS)
@languageCB
async def slider_queries(client: Client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    (what, rtype, query, user_id, cplay, fplay) = callback_request.split("|")
    if CallbackQuery.from_user.id != int(user_id):
        try:
            return await CallbackQuery.answer(_["playcb_1"], show_alert=True)
        except:
            return
    what = str(what)
    rtype = int(rtype)
    if what == "F":
        if rtype == 9:
            query_type = 0
        else:
            query_type = int(rtype + 1)
        try:
            await CallbackQuery.answer(_["playcb_2"])
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(media=thumbnail, caption=_["play_10"].format(title.title(), duration_min), has_spoiler=True)
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass
    if what == "B":
        if rtype == 0:
            query_type = 9
        else:
            query_type = int(rtype - 1)
        try:
            await CallbackQuery.answer(_["playcb_2"])
        except:
            pass
        title, duration_min, thumbnail, vidid = await YouTube.slider(query, query_type)
        buttons = slider_markup(_, vidid, user_id, query, query_type, cplay, fplay)
        med = InputMediaPhoto(media=thumbnail, caption=_["play_10"].format(title.title(), duration_min), has_spoiler=True)
        try:
            await CallbackQuery.edit_message_media(media=med, reply_markup=InlineKeyboardMarkup(buttons))
        except:
            pass

async def stream(client, _, mystic, user_id, result, chat_id, user_name, original_chat_id, video: Union[bool, str] = None, streamtype: Union[bool, str] = None, spotify: Union[bool, str] = None, forceplay: Union[bool, str] = None, userbot=None):
    try:
        a = await client.get_me()
        C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(a.id)
        if C_BOT_SUPPORT_CHAT:
            C_SUPPORT_CHAT = C_BOT_SUPPORT_CHAT if "https://" in C_BOT_SUPPORT_CHAT else f"https://t.me/{C_BOT_SUPPORT_CHAT}"
        else:
            C_SUPPORT_CHAT = config.SUPPORT_CHAT
    except:
        C_SUPPORT_CHAT = config.SUPPORT_CHAT
    if not result:
        return
    if forceplay:
        await Lucky.force_stop_stream(chat_id)
    
    bot_id = client.me.id
    bot_username = client.me.username # ✅ Added for Clone Buttons
    custom_caption = await get_clone_stream_caption(bot_id)

    if streamtype == "playlist":
        msg = f"{_['play_19']}\n\n"
        count = 0
        for search in result:
            if int(count) == config.PLAYLIST_FETCH_LIMIT:
                continue
            try:
                (title, duration_min, duration_sec, thumbnail, vidid) = await YouTube.details(search, False if spotify else True)
            except:
                continue
            if str(duration_min) == "None":
                continue
            if duration_sec > config.DURATION_LIMIT:
                continue
            if await is_active_chat(chat_id):
                await put_queue(chat_id, original_chat_id, f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio")
                db[chat_id][-1]["client"] = client
                position = len(db.get(chat_id)) - 1
                count += 1
                msg += f"{count}. {title[:70]}\n"
                msg += f"{_['play_20']} {position}\n\n"
            else:
                if not forceplay:
                    db[chat_id] = []
                status = True if video else None
                try:
                    file_path, direct = await YouTube.download(vidid, mystic, video=status, videoid=True)
                except:
                    continue
                await Lucky.join_call(chat_id, original_chat_id, file_path, video=status, image=thumbnail, userbot=userbot)
                await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio", forceplay=forceplay)
                db[chat_id][-1]["client"] = client
                img = await get_thumb(vidid, user_id, client)
                
                # ✅ Pass bot_username to buttons
                button = panel_markup_clone(_, vidid, chat_id)
                
                link = f"https://t.me/{client.me.username}?start=info_{vidid}"
                if custom_caption:
                    try:
                        final_caption = custom_caption.format(link, title[:25], duration_min, user_name)
                    except:
                        final_caption = _["stream_1"].format(link, title[:25], duration_min, user_name)
                else:
                    final_caption = _["stream_1"].format(link, title[:25], duration_min, user_name)

                run = await client.send_photo(original_chat_id, photo=img, caption=final_caption, reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
                db[chat_id][0]["mystic"] = run
                db[chat_id][0]["markup"] = "stream"
        if count == 0:
            return
        else:
            link = await LuckyBin(msg)
            upl = close_markup(_)
            return await client.send_message(original_chat_id, text=_["play_21"].format(position, link), reply_markup=upl)

    elif streamtype == "youtube":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        duration_min = result["duration_min"]
        thumbnail = result["thumb"]
        status = True if video else None
        try:
            file_path, direct = await YouTube.download(vidid, mystic, videoid=True, video=status)
        except:
            return await mystic.edit_text("❌ Error downloading video.")
        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio")
            db[chat_id][-1]["client"] = client
            img = await get_thumb(vidid, user_id, client)
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await client.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:18], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await Lucky.join_call(chat_id, original_chat_id, file_path, video=status, image=thumbnail, userbot=userbot)
            await put_queue(chat_id, original_chat_id, file_path if direct else f"vid_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio", forceplay=forceplay)
            db[chat_id][-1]["client"] = client
            img = await get_thumb(vidid, user_id, client)
            
            # ✅ Pass bot_username to buttons
            button = panel_markup_clone(_, vidid, chat_id)
            
            link = f"https://t.me/{client.me.username}?start=info_{vidid}"
            if custom_caption:
                try:
                    final_caption = custom_caption.format(link, title[:25], duration_min, user_name)
                except:
                    final_caption = _["stream_1"].format(link, title[:25], duration_min, user_name)
            else:
                final_caption = _["stream_1"].format(link, title[:25], duration_min, user_name)

            run = await client.send_photo(original_chat_id, photo=img, caption=final_caption, reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "stream"
            
    elif streamtype == "soundcloud":
        file_path = result["filepath"]
        title = result["title"]
        duration_min = result["duration_min"]
        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "audio")
            db[chat_id][-1]["client"] = client
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await client.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:18], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await Lucky.join_call(chat_id, original_chat_id, file_path, video=None, userbot=userbot)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "audio", forceplay=forceplay)
            db[chat_id][-1]["client"] = client
            
            # ✅ Pass bot_username to buttons
            button = stream_markup2(_, chat_id, bot_username)
            
            sc_img = get_random_img(config.SOUNCLOUD_IMG_URL)
            
            run = await client.send_photo(original_chat_id, photo=sc_img, caption=_["stream_1"].format(C_SUPPORT_CHAT, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "telegram":
        file_path = result["path"]
        link = result["link"]
        title = (result["title"]).title()
        duration_min = result["dur"]
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "video" if video else "audio")
            db[chat_id][-1]["client"] = client
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await client.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:18], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            await Lucky.join_call(chat_id, original_chat_id, file_path, video=status, userbot=userbot)
            await put_queue(chat_id, original_chat_id, file_path, title, duration_min, user_name, streamtype, user_id, "video" if video else "audio", forceplay=forceplay)
            db[chat_id][-1]["client"] = client
            if video: await add_active_video_chat(chat_id)
            
            # ✅ Pass bot_username to buttons
            button = stream_markup2(_, chat_id, bot_username)
            
            tg_img = get_random_img(config.TELEGRAM_VIDEO_URL) if video else get_random_img(config.TELEGRAM_AUDIO_URL)
                
            run = await client.send_photo(original_chat_id, photo=tg_img, caption=_["stream_1"].format(link, title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "live":
        link = result["link"]
        vidid = result["vidid"]
        title = (result["title"]).title()
        thumbnail = result["thumb"]
        duration_min = "Live Track"
        status = True if video else None
        if await is_active_chat(chat_id):
            await put_queue(chat_id, original_chat_id, f"live_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio")
            db[chat_id][-1]["client"] = client
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await client.send_message(chat_id=original_chat_id, text=_["queue_4"].format(position, title[:18], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button))
        else:
            if not forceplay:
                db[chat_id] = []
            n, file_path = await YouTube.video(link)
            if n == 0: raise AssistantErr(_["str_3"])
            await Lucky.join_call(chat_id, original_chat_id, file_path, video=status, image=thumbnail if thumbnail else None, userbot=userbot)
            await put_queue(chat_id, original_chat_id, f"live_{vidid}", title, duration_min, user_name, vidid, user_id, "video" if video else "audio", forceplay=forceplay)
            db[chat_id][-1]["client"] = client
            img = await get_thumb(vidid, user_id, client)
            i = await client.get_me()
            
            # ✅ Pass bot_username to buttons
            button = stream_markup2(_, chat_id, bot_username)
            
            run = await client.send_photo(original_chat_id, photo=img, caption=_["stream_1"].format(f"https://t.me/{i.username}?start=info_{vidid}", title[:23], duration_min, user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"

    elif streamtype == "index":
        link = result
        title = "Index or M3u8 Link"
        duration_min = "00:00"
        if await is_active_chat(chat_id):
            await put_queue_index(chat_id, original_chat_id, "index_url", title, duration_min, user_name, link, "video" if video else "audio")
            db[chat_id][-1]["client"] = client
            position = len(db.get(chat_id)) - 1
            button = aq_markup(_, chat_id)
            await mystic.edit_text("**Added to Queue.**")
        else:
            if not forceplay:
                db[chat_id] = []
            await Lucky.join_call(chat_id, original_chat_id, link, video=True if video else None, userbot=userbot)
            await put_queue_index(chat_id, original_chat_id, "index_url", title, duration_min, user_name, link, "video" if video else "audio", forceplay=forceplay)
            db[chat_id][-1]["client"] = client
            
            # ✅ Pass bot_username to buttons
            button = stream_markup2(_, chat_id, bot_username)
            
            stream_img = get_random_img(config.STREAM_IMG_URL)

            run = await client.send_photo(original_chat_id, photo=stream_img, caption=_["stream_2"].format(user_name), reply_markup=InlineKeyboardMarkup(button), has_spoiler=True)
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
            await mystic.delete()