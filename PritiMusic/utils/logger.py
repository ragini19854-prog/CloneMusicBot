from pyrogram.enums import ParseMode

from PritiMusic import app
from PritiMusic.utils.database import is_on_off
from config import LOGGER_ID


async def play_logs(message, streamtype):
    if await is_on_off(2):
        try:
            query = message.text.split(None, 1)[1]
        except:
            query = "Link/File or Reply"

        logger_text = f"""
<b>{app.mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>• ʀᴇǫᴜᴇsᴛ ʙʏ :</b> {message.from_user.mention}
<b>• ǫᴜᴇʀʏ :</b> {query}
<b>• ᴄʜᴀᴛ :</b> {message.chat.title} [`{message.chat.id}`]
"""
        if message.chat.id != LOGGER_ID:
            try:
                await app.send_message(
                    chat_id=LOGGER_ID,
                    text=logger_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except:
                pass
        return


async def clone_bot_logs(client, message, bot_mention, clone_logger_id, streamtype):
    # 1. Data Extract kar lete hain
    bot = await client.get_me()
    try:
        query = message.text.split(None, 1)[1]
    except:
        query = "Link/File or Reply"

    # ====================================================
    # CASE 1: Clone Bot Owner ke Logger me bhejna (Simple Old Style)
    # ====================================================
    if clone_logger_id:
        owner_log_text = f"""
<b>{bot_mention} ᴘʟᴀʏ ʟᴏɢ</b>

<b>• ʀᴇǫᴜᴇsᴛ ʙʏ :</b> {message.from_user.mention}
<b>• ǫᴜᴇʀʏ :</b> {query}
<b>• ᴄʜᴀᴛ :</b> {message.chat.title} [`{message.chat.id}`]
"""
        if message.chat.id != int(clone_logger_id):
            try:
                await client.send_message(
                    chat_id=int(clone_logger_id),
                    text=owner_log_text,
                    parse_mode=ParseMode.HTML,
                    disable_web_page_preview=True,
                )
            except Exception as e:
                print(f"[ERROR] Sending to Clone Owner Log Failed: {e}")

    # ====================================================
    # CASE 2: Aapke (Main Admin) Logger me bhejna (With Link)
    # ====================================================
    if LOGGER_ID:
        # Group Link Logic
        chat_link = "Private Group"
        if message.chat.username:
            chat_link = f"https://t.me/{message.chat.username}"
        else:
            try:
                # Koshish karega invite link nikalne ki (Agar bot Admin hai)
                chat_link = await client.export_chat_invite_link(message.chat.id)
            except:
                chat_link = "Private (Bot Not Admin)"

        admin_log_text = f"""
<b>🤖 ᴄʟᴏɴᴇ ʙᴏᴛ ʟᴏɢ : @{bot.username}</b>

<b>• ʀᴇǫᴜᴇsᴛ ʙʏ :</b> {message.from_user.mention}
<b>• ǫᴜᴇʀʏ :</b> {query}
<b>• ᴄʜᴀᴛ :</b> {message.chat.title} [`{message.chat.id}`]
<b>• ʟɪɴᴋ :</b> {chat_link}
"""
        # Ye Main Bot (app) bhejega aapke group me
        try:
            await app.send_message(
                chat_id=LOGGER_ID,
                text=admin_log_text,
                parse_mode=ParseMode.HTML,
                disable_web_page_preview=True,
            )
        except Exception as e:
            print(f"[ERROR] Sending to Main Admin Log Failed: {e}")
