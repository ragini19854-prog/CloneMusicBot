import asyncio
import random
from pyrogram.types import CallbackQuery, InputMediaVideo, InputMediaPhoto, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters

from MadaraMusic import YouTube, app
from MadaraMusic.core.call import Lucky
from MadaraMusic.misc import SUDOERS, db
from MadaraMusic.utils.database import (
    get_active_chats, get_lang, get_upvote_count, is_active_chat,
    is_music_playing, is_nonadmin_chat, music_off, music_on, set_loop, get_assistant
)
from MadaraMusic.utils.decorators.language import languageCB
from MadaraMusic.utils.formatters import seconds_to_min
from MadaraMusic.utils.inline import close_markup, stream_markup, stream_markup_timer
from MadaraMusic.utils.stream.autoclear import auto_clean
from MadaraMusic.utils.thumbnails import get_thumb
import config
from config import (
    BANNED_USERS, SOUNCLOUD_IMG_URL, STREAM_IMG_URL, TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL, START_IMG_URL, adminlist, confirmer, votemode
)
from strings import get_string
from MadaraMusic.utils.inline.start import private_panel, support_panel

checker = {}
upvoters = {}

# --- BACK BUTTON HANDLER (Fix for Video/Photo + Random Image) ---
@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_helper(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass
    
    # Agar START_IMG_URL list hai to random choice karega, nahi to direct string lega
    if isinstance(START_IMG_URL, list):
        img = random.choice(START_IMG_URL)
    else:
        img = START_IMG_URL

    await CallbackQuery.edit_message_media(
        media=InputMediaPhoto(
            media=img,
            caption=_["start_2"].format(CallbackQuery.from_user.mention, app.mention)
        ),
        reply_markup=InlineKeyboardMarkup(private_panel(_))
    )

# --- SUPPORT PAGE ---
@app.on_callback_query(filters.regex("support_page") & ~BANNED_USERS)
async def support_cb(client, callback_query):
    try:
        _ = get_string("en")
        await callback_query.answer()
        await callback_query.edit_message_reply_markup(
            reply_markup=InlineKeyboardMarkup(support_panel(_))
        )
    except Exception as e:
        await callback_query.answer(f"Error: {e}", show_alert=True)

# --- CLONE PAGE ---
@app.on_callback_query(filters.regex("clone_page") & ~BANNED_USERS)
@languageCB
async def clone_page_cb(client, CallbackQuery, _):
    await CallbackQuery.answer()
    clone_text = (
        "**ᴍᴀᴋᴇ ʏᴏᴜʀ ᴏᴡɴ ᴍᴜsɪᴄ ʙᴏᴛ ᴡᴀᴛᴄʜɪɴɢ ᴛʜᴇ ᴠɪᴅᴇᴏ ᴄᴀʀᴇғᴜʟʟʏ.**\n\n"
        "<blockquote><b><u>ᴄʟᴏɴᴇ ᴄᴏᴍᴍᴀɴᴅs :</u></b>\n\n"
        "<b><u>ᴀʟʟ ᴜsᴇʀs :</u></b>\n"
        "/clone – <b>ᴄʟᴏɴᴇ ʏᴏᴜʀ ᴏᴡɴ ʙᴏᴛ ᴜsɪɴɢ ʙᴏᴛ ᴛᴏᴋᴇɴ ғʀᴏᴍ @BotFather.</b>\n"
        "<b>ᴇxᴀᴍᴘʟᴇ:</b> /clone <code>ᴘᴀsᴛᴇ_ᴛᴏᴋᴇɴ_ʜᴇʀᴇ</code>\n\n"
        "/rmbot – <b>ᴅᴇʟᴇᴛᴇ ʏᴏᴜʀ ᴄʟᴏɴᴇᴅ ʙᴏᴛ.</b>\n\n"
        "/mybot – <b>ᴄʜᴇᴄᴋ ᴛʜᴇ ʙᴏᴛs ʏᴏᴜ'ᴠᴇ ᴄʟᴏɴᴇᴅ.</b></blockquote>"
    )
    await CallbackQuery.edit_message_media(
        media=InputMediaVideo(
            media="https://files.catbox.moe/rxiwb3.mp4",
            caption=clone_text
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="🎁 ᴅᴏɴᴀᴛᴇ (₹𝟷𝟶)", callback_data="donate_Madara")],
                [InlineKeyboardButton(text="⌯ ʙᴀᴄᴋ ⌯", callback_data="settingsback_helper")]
            ]
        )
    )

# --- SOURCE PAGE (Video + Owner + Back) ---
@app.on_callback_query(filters.regex("gib_source") & ~BANNED_USERS)
@languageCB
async def gib_source_cb(client, CallbackQuery, _):
    await CallbackQuery.answer()
    source_text = (
        𝐏ʟᴇᴀꜱᴇ 𝐂ʟɪᴄᴋ 𝐎ɴ 𝐒ᴏᴜʀᴄᴇ 𝐂ᴏᴅᴇ 𝐁ᴜᴛᴛᴏɴ 𝐁ᴇʟᴏᴡ !
       <pre>||➥ᴜᴘᴛɪᴍᴇ: 𝟷ʜ:𝟹𝟺ᴍ:𝟻𝟺s
       ➥sᴇʀᴠᴇʀ sᴛᴏʀᴀɢᴇ: 𝟸𝟽.𝟺%
       ➥ᴄᴘᴜ ʟᴏᴀᴅ: 𝟷𝟷.𝟸%
       ➥ʀᴀᴍ ᴄᴏɴsᴜᴍᴘᴛɪᴏɴ: 𝟷𝟽.𝟻%||</pre>
       •──────────────────•
       ᴘᴏᴡєʀєᴅ ʙʏ»|| [˹ 𝐅ᴜᴄᴋᴇʀ ꭙ 𝐎ᴡɴᴇʀ ♪˼](https://t.me/YOUR_fucker_dad)||
       •──────────────────•
    )
    await CallbackQuery.edit_message_media(
        media=InputMediaVideo(
            media="https://files.catbox.moe/rxiwb3.mp4",
            caption=source_text
        ),
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="ᴏᴡɴᴇʀ", user_id=config.OWNER_ID)],
                [InlineKeyboardButton(text="⌯ ʙᴀᴄᴋ ⌯", callback_data="settingsback_helper")]
            ]
        )
    )

# --- DONATE PAGE ---
@app.on_callback_query(filters.regex("donate_Madara") & ~BANNED_USERS)
@languageCB
async def donate_callback(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer("Support our hardwork! ❤️")
    except:
        pass
    
    donate_text = """
<blockquote expandable><b><u>❤️ sᴜᴘᴘᴏʀᴛ ᴍᴜsɪᴄ ʙᴏᴛ</u></b>
<b>ɪ ᴡᴏʀᴋ ʜᴀʀᴅ ᴛᴏ ᴍᴀᴋᴇ ᴛʜᴇsᴇ ᴀᴍᴀᴢɪɴɢ ᴍᴜsɪᴄ ʙᴏᴛs ғᴏʀ ʏᴏᴜ.</b>
<b>ᴘʟᴇᴀsᴇ ᴅᴏɴᴀᴛᴇ ᴏɴʟʏ ₹𝟷𝟶.</b>
<b>sᴄᴀɴ ᴛʜᴇ ǫʀ ᴄᴏᴅᴇ ᴀʙᴏᴠᴇ ᴛᴏ ᴅᴏɴᴀᴛᴇ.</b>
<b>ᴛʜᴀɴᴋ ʏᴏᴜ ғᴏʀ ʏᴏᴜʀ ʟᴏᴠᴇ! ✨</b></blockquote>
"""
    await CallbackQuery.edit_message_media(
        media=InputMediaPhoto(
            media="https://i.ibb.co/Hfhp24mq/image.jpg",
            caption=donate_text
        ),
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton(text="⌯ ʙᴀᴄᴋ ⌯", callback_data="clone_page")]]
        )
    )

# --- UNBAN ASSISTANT ---
@app.on_callback_query(filters.regex("unban_assistant"))
async def unban_assistant(_, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    userbot = await get_assistant(chat_id)
    try:
        await app.unban_chat_member(chat_id, userbot.id)
        await callback.answer("Assistant Unbanned Successfully!", show_alert=True)
    except Exception:
        await callback.answer("Failed to unban. Give me Admin permissions.", show_alert=True)

# --- ADMIN COMMANDS ---
@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
    mention = CallbackQuery.from_user.mention
    
    if command == "UpVote":
        if chat_id not in votemode: votemode[chat_id] = {}
        if chat_id not in upvoters: upvoters[chat_id] = {}
        
        voters = (upvoters[chat_id]).get(CallbackQuery.message.id)
        if not voters: upvoters[chat_id][CallbackQuery.message.id] = []
        
        vote = (votemode[chat_id]).get(CallbackQuery.message.id)
        if not vote: votemode[chat_id][CallbackQuery.message.id] = 0
        
        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            (upvoters[chat_id][CallbackQuery.message.id]).remove(CallbackQuery.from_user.id)
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            (upvoters[chat_id][CallbackQuery.message.id]).append(CallbackQuery.from_user.id)
            votemode[chat_id][CallbackQuery.message.id] += 1
            
        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])
        
        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
                if current["vidid"] != exists["vidid"] or current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message_text(_["admin_35"])
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])
            try:
                await CallbackQuery.edit_message_text(_["admin_37"].format(upvote))
            except:
                pass
            command = counter
            mention = "ᴜᴘᴠᴏᴛᴇs"
        else:
            if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
                await CallbackQuery.answer(_["admin_38"], show_alert=True)
            else:
                await CallbackQuery.answer(_["admin_39"], show_alert=True)
            upl = InlineKeyboardMarkup([[InlineKeyboardButton(text=f"👍 {get_upvotes}", callback_data=f"ADMIN  UpVote|{chat_id}_{counter}")]])
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)
    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                if not admins or CallbackQuery.from_user.id not in admins:
                    return await CallbackQuery.answer(_["admin_14"], show_alert=True)
                    
    if command == "Pause":
        if not await is_music_playing(chat_id): return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await CallbackQuery.answer()
        await music_off(chat_id)
        await Lucky.pause_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_2"].format(mention), reply_markup=close_markup(_))
    elif command == "Resume":
        if await is_music_playing(chat_id): return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await CallbackQuery.answer()
        await music_on(chat_id)
        await Lucky.resume_stream(chat_id)
        await CallbackQuery.message.reply_text(_["admin_4"].format(mention), reply_markup=close_markup(_))
    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await Lucky.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(_["admin_5"].format(mention), reply_markup=close_markup(_))
        await CallbackQuery.message.delete()
    elif command == "Skip" or command == "Replay":
        check = db.get(chat_id)
        if command == "Skip":
            txt = f"➻ sᴛʀᴇᴀᴍ sᴋɪᴩᴩᴇᴅ 🎄\n│ \n└ʙʏ : {mention} 🥀"
            try:
                popped = check.pop(0)
                if popped: await auto_clean(popped)
                if not check:
                    await CallbackQuery.edit_message_text(txt)
                    await CallbackQuery.message.reply_text(_["admin_6"].format(mention, CallbackQuery.message.chat.title), reply_markup=close_markup(_))
                    return await Lucky.stop_stream(chat_id)
            except:
                return await Lucky.stop_stream(chat_id)
        else:
            txt = f"➻ sᴛʀᴇᴀᴍ ʀᴇ-ᴘʟᴀʏᴇᴅ 🎄\n│ \n└ʙʏ : {mention} 🥀"
        
        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        duration = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0
        
        try:
            image = await YouTube.thumbnail(videoid, True)
        except:
            image = None
            
        try:
            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0: return await CallbackQuery.message.reply_text(_["admin_7"].format(title))
                await Lucky.skip_stream(chat_id, link, video=status, image=image)
            elif "vid_" in queued:
                 await Lucky.skip_stream(chat_id, queued, video=status, image=image)
            else:
                 await Lucky.skip_stream(chat_id, queued, video=status, image=image)
        except:
            return await CallbackQuery.message.reply_text(_["call_6"])

        button = stream_markup(_, chat_id)
        img = await get_thumb(videoid)
        run = await CallbackQuery.message.reply_photo(
            photo=img if img else STREAM_IMG_URL,
            caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{videoid}", title[:23], duration, user),
            reply_markup=InlineKeyboardMarkup(button),
        )
        db[chat_id][0]["mystic"] = run
        db[chat_id][0]["markup"] = "tg"
        await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))

async def markup_timer():
    while not await asyncio.sleep(7):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id): continue
                playing = db.get(chat_id)
                if not playing or int(playing[0]["seconds"]) == 0: continue
                mystic = playing[0]["mystic"]
                try:
                    if checker[chat_id][mystic.id] is False: continue
                except: pass
                
                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except: _ = get_string("en")
                
                try:
                    buttons = stream_markup_timer(_, chat_id, seconds_to_min(playing[0]["played"]), playing[0]["dur"])
                    await mystic.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except: continue
            except: continue

asyncio.create_task(markup_timer())
