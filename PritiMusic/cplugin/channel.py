from time import time
import asyncio
from pyrogram import filters, Client
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, ChatType
from pyrogram.types import Message

from PritiMusic import app
from PritiMusic.utils.database import set_cmode
from PritiMusic.utils.decorators.admins import AdminActual
from config import BANNED_USERS

# Spam Protection Memory
user_last_message_time = {}
user_command_count = {}
SPAM_THRESHOLD = 2
SPAM_WINDOW_SECONDS = 5

@Client.on_message(filters.command(["channelplay"]) & filters.group & ~BANNED_USERS)
@AdminActual
async def playmode_(client, message: Message, _):
    user_id = message.from_user.id
    current_time = time()
    
    # Spam Logic
    last_message_time = user_last_message_time.get(user_id, 0)

    if current_time - last_message_time < SPAM_WINDOW_SECONDS:
        user_last_message_time[user_id] = current_time
        user_command_count[user_id] = user_command_count.get(user_id, 0) + 1
        if user_command_count[user_id] > SPAM_THRESHOLD:
            hu = await message.reply_text(
                f"**{message.from_user.mention} ᴘʟᴇᴀsᴇ ᴅᴏɴᴛ ᴅᴏ sᴘᴀᴍ, ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴀғᴛᴇʀ 5 sᴇᴄ**"
            )
            await asyncio.sleep(3)
            await hu.delete()
            return
    else:
        user_command_count[user_id] = 1
        user_last_message_time[user_id] = current_time

    # Command Logic
    if len(message.command) < 2:
        return await message.reply_text(_["cplay_1"].format(message.chat.title))
    
    query = message.text.split(None, 2)[1].lower().strip()
    
    # Option 1: Disable
    if str(query) == "disable":
        await set_cmode(message.chat.id, None)
        return await message.reply_text(_["cplay_7"])
    
    # Option 2: Linked Chat
    elif str(query) == "linked":
        chat = await client.get_chat(message.chat.id)
        if chat.linked_chat:
            chat_id = chat.linked_chat.id
            await set_cmode(message.chat.id, chat_id)
            return await message.reply_text(
                _["cplay_3"].format(chat.linked_chat.title, chat.linked_chat.id)
            )
        else:
            return await message.reply_text(_["cplay_2"])
    
    # Option 3: Custom Channel ID/Username
    else:
        try:
            chat = await client.get_chat(query)
        except:
            return await message.reply_text(_["cplay_4"])
        
        if chat.type != ChatType.CHANNEL:
            return await message.reply_text(_["cplay_5"])
        
        # Verify Ownership
        crid = None
        cusn = None
        try:
            async for user in client.get_chat_members(
                chat.id, filter=ChatMembersFilter.ADMINISTRATORS
            ):
                if user.status == ChatMemberStatus.OWNER:
                    cusn = user.user.username
                    crid = user.user.id
                    break 
        except:
            return await message.reply_text(_["cplay_4"])
            
        if crid != message.from_user.id:
            return await message.reply_text(_["cplay_6"].format(chat.title, cusn))
            
        await set_cmode(message.chat.id, chat.id)
        return await message.reply_text(_["cplay_3"].format(chat.title, chat.id))
