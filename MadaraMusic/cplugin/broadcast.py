import asyncio
from pyrogram import filters, Client
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from MadaraMusic import app
from MadaraMusic.utils.database import (
    get_served_chats_clone,
    get_served_users_clone,
)
from MadaraMusic.utils.database.clonedb import get_owner_id_from_db
from MadaraMusic.utils.decorators.language import language
from config import OWNER_ID, SUPPORT_CHAT

# Global flag to prevent overlapping broadcasts
IS_BROADCASTING = False

@Client.on_message(filters.command(["broadcast"]))
@language
async def broadcast_message(client, message: Message, _):
    global IS_BROADCASTING
    
    # 1. Identify the current bot instance
    bot_obj = await client.get_me()
    bot_id = bot_obj.id
    
    # 2. Verify Ownership
    try:
        clone_owner_id = await get_owner_id_from_db(bot_id)
    except:
        clone_owner_id = get_owner_id_from_db(bot_id)
        
    # Allow only the Main Owner and the Specific Clone Bot Owner
    if message.from_user.id not in [OWNER_ID, clone_owner_id]:
        return await message.reply_text(_["c_brod_1"].format(SUPPORT_CHAT))

    if IS_BROADCASTING:
        return await message.reply_text("⏳ **Broadcast is already running. Please wait.**")

    # 3. Parse Command and Query
    query = ""
    if message.reply_to_message:
        query = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
    else:
        if len(message.command) < 2:
            return await message.reply_text(_["broad_2"])
        query = message.text.split(None, 1)[1]

    # Clean flags from the text to be sent
    flags = ["-pin", "-nobot", "-pinloud", "-user"]
    query_to_send = query
    for flag in flags:
        query_to_send = query_to_send.replace(flag, "").strip()

    if not message.reply_to_message and not query_to_send:
        return await message.reply_text(_["broad_8"])

    # Start Broadcast
    IS_BROADCASTING = True
    status_msg = await message.reply_text(_["broad_1"])

    try:
        # --- PART A: BROADCAST TO GROUPS ---
        if "-nobot" not in message.text:
            sent = 0
            pin_count = 0
            
            # Fetch chats served specifically by this bot_id
            served_chats = await get_served_chats_clone(bot_id)
            
            for chat in served_chats:
                try:
                    chat_id = int(chat["chat_id"])
                    
                    # Forward or Send
                    if message.reply_to_message:
                        m = await client.forward_messages(
                            chat_id, 
                            message.chat.id, 
                            message.reply_to_message.id
                        )
                    else:
                        m = await client.send_message(chat_id, text=query_to_send)
                    
                    # Pin Logic
                    if "-pin" in message.text or "-pinloud" in message.text:
                        try:
                            msg_obj = m[0] if isinstance(m, list) else m
                            notify = "-pinloud" in message.text
                            await msg_obj.pin(disable_notification=not notify)
                            pin_count += 1
                        except:
                            pass
                            
                    sent += 1
                    await asyncio.sleep(0.2) 
                    
                except FloodWait as fw:
                    await asyncio.sleep(int(fw.value))
                except Exception:
                    continue
            
            await message.reply_text(_["broad_3"].format(sent, pin_count))

        # --- PART B: BROADCAST TO USERS ---
        if "-user" in message.text:
            susr = 0
            
            # Fetch users served specifically by this bot_id
            served_users = await get_served_users_clone(bot_id)
            
            for user in served_users:
                try:
                    user_id = int(user["user_id"])
                    
                    if message.reply_to_message:
                        await client.forward_messages(
                            user_id, 
                            message.chat.id, 
                            message.reply_to_message.id
                        )
                    else:
                        await client.send_message(user_id, text=query_to_send)
                        
                    susr += 1
                    await asyncio.sleep(0.2)
                    
                except FloodWait as fw:
                    await asyncio.sleep(int(fw.value))
                except Exception:
                    pass
            
            await message.reply_text(_["broad_4"].format(susr))

    finally:
        # Ensure the lock is released even if errors occur
        IS_BROADCASTING = False
