from pyrogram import Client, filters
from pyrogram.types import Message
from MadaraMusic.utils.database.clonedb import (
    set_clone_search_type, 
    get_clone_search_type,
    set_clone_stream_caption,
    delete_clone_search_type,
    delete_clone_stream_caption,
    get_owner_id_from_db
)

# --- HELPER FUNCTIONS ---

async def is_clone_owner(client: Client, message: Message):
    bot_id = client.me.id
    try:
        owner_id = await get_owner_id_from_db(bot_id)
    except:
        owner_id = get_owner_id_from_db(bot_id)
        
    if message.from_user.id != owner_id:
        await message.reply_text("❌ **Only the Bot Owner can change these settings.**")
        return False
    return True

async def add_to_random_list(bot_id, type_key, new_value):
    current_data = await get_clone_search_type(bot_id, type_key)
    
    if current_data:
        if new_value in current_data:
            return False 
        final_value = f"{current_data}|||{new_value}"
    else:
        final_value = new_value
    
    await set_clone_search_type(bot_id, type_key, final_value)
    return True

# ==========================================
#              SETTING COMMANDS
# ==========================================

# --- 1. TEXT & EMOJI ---
@Client.on_message(filters.command(["setplaytext", "addplaytext"]))
async def set_play_text(client, message: Message):
    if not await is_clone_owner(client, message):
        return

    if len(message.command) < 2:
        return await message.reply_text("Usage: /setplaytext <Text/Emoji>")
    
    text = message.text.split(None, 1)[1]
    bot_id = client.me.id
    
    await add_to_random_list(bot_id, "text", text)
    await message.reply_text(f"✅ **Added to Random List:**\n\n{text}")

# --- 2. STICKER ---
@Client.on_message(filters.command(["setplaysticker", "addplaysticker"]))
async def set_play_sticker(client, message: Message):
    if not await is_clone_owner(client, message):
        return

    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("Usage: Reply to a Sticker with /setplaysticker")
    
    file_id = message.reply_to_message.sticker.file_id
    bot_id = client.me.id
    
    await add_to_random_list(bot_id, "sticker", file_id)
    await message.reply_text("✅ **Sticker Added to Random List!**")

# --- 3. ANIMATION (GIF) ---
@Client.on_message(filters.command(["setplayanimation", "addplayanimation"]))
async def set_play_gif(client, message: Message):
    if not await is_clone_owner(client, message):
        return

    if not message.reply_to_message or not message.reply_to_message.animation:
        return await message.reply_text("Usage: Reply to a GIF with /setplayanimation")
    
    file_id = message.reply_to_message.animation.file_id
    bot_id = client.me.id
    
    await add_to_random_list(bot_id, "animation", file_id)
    
    # Auto-Hide Text
    current_text = await get_clone_search_type(bot_id, "text")
    if not current_text:
        await set_clone_search_type(bot_id, "text", "⠀")
        
    await message.reply_text("✅ **GIF Added to Random List!**")

# --- 4. VIDEO (MP4) ---
@Client.on_message(filters.command(["setplayvideo", "addplayvideo"]))
async def set_play_video(client, message: Message):
    if not await is_clone_owner(client, message):
        return

    if not message.reply_to_message or not message.reply_to_message.video:
        return await message.reply_text("Usage: Reply to a Video with /setplayvideo")
    
    file_id = message.reply_to_message.video.file_id
    bot_id = client.me.id
    
    await add_to_random_list(bot_id, "video", file_id)
    
    # Auto-Hide Text
    current_text = await get_clone_search_type(bot_id, "text")
    if not current_text:
        await set_clone_search_type(bot_id, "text", "⠀")
    
    await message.reply_text("✅ **Video Added to Random List!**\n(Searching text hidden automatically)")

# --- 5. PHOTO (IMAGE) ---
@Client.on_message(filters.command(["setplayphoto", "addplayphoto"]))
async def set_play_photo(client, message: Message):
    if not await is_clone_owner(client, message):
        return

    if not message.reply_to_message or not message.reply_to_message.photo:
        return await message.reply_text("Usage: Reply to a Photo with /setplayphoto")
    
    file_id = message.reply_to_message.photo.file_id
    bot_id = client.me.id
    
    await add_to_random_list(bot_id, "photo", file_id)
    
    # Auto-Hide Text
    current_text = await get_clone_search_type(bot_id, "text")
    if not current_text:
        await set_clone_search_type(bot_id, "text", "⠀")
    
    await message.reply_text("✅ **Photo Added to Random List!**")

# --- 6. CAPTION SETTING ---
@Client.on_message(filters.command("setstreamtext"))
async def set_stream_text(client, message: Message):
    if not await is_clone_owner(client, message):
        return

    if len(message.command) < 2:
        return await message.reply_text(
            "**Usage:** /setstreamtext <Your Caption>\n\n"
            "**Available Variables:**\n"
            "`{1}` : Song Name\n"
            "`{2}` : Duration\n"
            "`{3}` : Requested By\n\n"
            "**Example:**\n"
            "`/setstreamtext 🎸 Playing: {1} | ⏳ Time: {2}`"
        )
    
    text = message.text.split(None, 1)[1]
    bot_id = client.me.id
    
    await set_clone_stream_caption(bot_id, text)
    await message.reply_text(f"✅ **Stream Caption Updated:**\n\n{text}")

# ==========================================
#              DELETE / RESET COMMANDS
# ==========================================

@Client.on_message(filters.command(["delplay", "resetplay", "delplaymode"]))
async def delete_play_mode(client, message: Message):
    if not await is_clone_owner(client, message):
        return
        
    bot_id = client.me.id
    await delete_clone_search_type(bot_id)
    await message.reply_text("🗑️ **Search Mode Reset!**\nAll saved random lists cleared.")

@Client.on_message(filters.command(["delstreamtext", "resetstreamtext"]))
async def delete_stream_text_cmd(client, message: Message):
    if not await is_clone_owner(client, message):
        return
        
    bot_id = client.me.id
    await delete_clone_stream_caption(bot_id)
    await message.reply_text("🗑️ **Stream Caption Reset!**")
