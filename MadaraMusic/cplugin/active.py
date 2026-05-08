from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from MadaraMusic.utils.database import (
    get_active_chats,
    get_active_video_chats,
)
from MadaraMusic.utils.database.clonedb import get_served_chats_clone, clonebotdb

@Client.on_message(filters.command(["ac", "activevc", "activevoice"]))
async def start(client: Client, message: Message):
    
    bot_id = client.me.id
    user_id = message.from_user.id
    
    # Fetch Owner from Database
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    
    if not clone_data:
        return 
        
    owner_id = clone_data.get("user_id")

    # STRICT OWNER CHECK
    if user_id != owner_id:
        return await message.reply_text("❌ **Only the Bot Owner can view these stats.**")

    waiting_msg = await message.reply_text("🔄 **Checking active groups...**")

    # DATA FETCHING
    global_audio = await get_active_chats()
    global_video = await get_active_video_chats()

    # Fetch Served Chats for this specific bot
    try:
        clone_served_chats = await get_served_chats_clone(bot_id)
        my_chat_ids = [int(chat["chat_id"]) for chat in clone_served_chats]
    except:
        my_chat_ids = []

    # FILTERING
    my_audio_count = 0
    for chat_id in global_audio:
        if chat_id in my_chat_ids:
            my_audio_count += 1

    my_video_count = 0
    for chat_id in global_video:
        if chat_id in my_chat_ids:
            my_video_count += 1

    # RESULT
    text = (
        f"📊 <b><u>Bot Activity Status</u></b>\n\n"
        f"👤 **Owner:** {message.from_user.mention}\n"
        f"🤖 **Bot:** @{client.me.username}\n\n"
        f"🏢 **Total Groups:** `{len(my_chat_ids)}`\n"
        f"🎧 **Active Audio:** `{my_audio_count}`\n"
        f"📹 **Active Video:** `{my_video_count}`\n"
    )
    
    await waiting_msg.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✯ Close ✯", callback_data=f"close")]]
        ),
    )
