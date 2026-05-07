import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from PritiMusic import app
from PritiMusic.utils.decorators.language import language
from PritiMusic.utils.database.clonedb import (
    get_owner_id_from_db,
    get_cloned_support_chat,
    get_cloned_support_channel
)
from PritiMusic.utils.database import clonebotdb
from config import SUPPORT_CHAT, OWNER_ID

# --- Helper Function: Clean URL/Username ---
def clean_url_or_username(value):
    if "t.me/+" in value or "joinchat" in value or "https://" in value or "http://" in value:
        return value.strip()
    
    value = value.replace("https://", "").replace("http://", "")
    value = value.replace("t.me/", "").replace("telegram.me/", "")
    value = value.replace("@", "")
    return value.strip("/")

# --- Logging Helper Functions (Async Fixed) ---
async def get_logging_status(bot_id):
    bot_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not bot_data:
        return True
    return bot_data.get("logging", True)

async def get_log_channel(bot_id):
    bot_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not bot_data:
        return "-100"
    return bot_data.get("logchannel", "-100")


# --- Commands ---

@Client.on_message(filters.command("setchannel"))
@language
async def set_channel(client: Client, message: Message, _):
    bot = await client.get_me()
    bot_id = bot.id

    C_OWNER = await get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))
    
    if len(message.command) != 2:
        return await message.reply_text(_["C_P_I_2"])
    
    raw_input = message.command[1]
    final_value = clean_url_or_username(raw_input)

    # Fixed: Added await for DB update
    result = await clonebotdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"channel": final_value}},
        upsert=True
    )
    
    if result.modified_count > 0 or result.upserted_id:
        await message.reply_text(_["C_P_I_4"].format(final_value))
    else:
        await message.reply_text(_["C_P_I_6"])


@Client.on_message(filters.command("setsupport"))
@language
async def set_support(client: Client, message: Message, _):
    bot = await client.get_me()
    bot_id = bot.id

    C_OWNER = await get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))
    
    if len(message.command) != 2:
        return await message.reply_text(_["C_P_I_1"])

    raw_input = message.command[1]
    final_value = clean_url_or_username(raw_input)

    # Fixed: Added await for DB update
    result = await clonebotdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"support": final_value}},
        upsert=True
    )
    
    if result.modified_count > 0 or result.upserted_id:
        await message.reply_text(_["C_P_I_3"].format(final_value))
    else:
        await message.reply_text(_["C_P_I_5"])


@Client.on_message(filters.command("botinfo"))
@language
async def bot_info(client: Client, message: Message, _):
    bot = await client.get_me()
    bot_id = bot.id

    C_OWNER = await get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))

    # Async calls to fetch data
    channel = await get_cloned_support_channel(bot_id)
    support = await get_cloned_support_chat(bot_id)
    
    await message.reply_text(
        f"**ʙᴏᴛ ɪɴғᴏ:**\n"
        f"➤ **ʙᴏᴛ ɪᴅ:** `{bot_id}`\n"
        f"➤ **ᴄʜᴀɴɴᴇʟ:** {channel}\n"
        f"➤ **sᴜᴘᴘᴏʀᴛ ᴄʜᴀᴛ:** {support}"
    )


@Client.on_message(filters.command("logstatus"))
@language
async def check_log_status(client: Client, message: Message, _):
    bot_id = client.me.id
    C_OWNER = await get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))

    # Fixed: Added await
    logging_status = await get_logging_status(bot_id)
    log_channel = await get_log_channel(bot_id)
    
    C_LOGGER_STATUS = "Enabled" if logging_status else "Disabled"
    C_LOGGER_VALUE = log_channel if str(log_channel) != "-100" else "Not Set"

    text = f"**ʟᴏɢɢᴇʀ sᴛᴀᴛᴜs :**\n\n - sᴛᴀᴛᴜs : `{C_LOGGER_STATUS}`\n - ʟᴏɢɢᴇʀ ɪᴅ : `{C_LOGGER_VALUE}`"
    await message.reply_text(text)


@Client.on_message(filters.command("logger"))
@language
async def toggle_logging(client: Client, message: Message, _):
    bot = await client.get_me()
    bot_id = bot.id
    C_OWNER = await get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))

    if len(message.command) != 2 or message.command[1].lower() not in ["enable", "disable"]:
        return await message.reply_text("**ᴇxᴀᴍᴘʟᴇ :** \n/logger [ᴇɴᴀʙʟᴇ | ᴅɪsᴀʙʟᴇ]")

    logging_status = message.command[1].lower() == "enable"
    
    # Fixed: Added await
    await clonebotdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"logging": logging_status}},
        upsert=True
    )
    await message.reply_text(f"{'ᴇɴᴀʙʟᴇᴅ' if logging_status else 'ᴅɪsᴀʙʟᴇᴅ'} ʟᴏɢɢɪɴɢ.")


@Client.on_message(filters.command("setlogger"))
@language
async def set_log_channel(client: Client, message: Message, _):
    bot = await client.get_me()
    bot_id = bot.id
    C_OWNER = await get_owner_id_from_db(bot_id)
    OWNERS = [OWNER_ID, C_OWNER]

    if message.from_user.id not in OWNERS:
        return await message.reply_text(_["NOT_C_OWNER"].format(SUPPORT_CHAT))

    if len(message.command) != 2:
        return await message.reply_text("**ᴇxᴀᴍᴘʟᴇ :** \n- `/setlogger -100xxxxxxxx`")

    try:
        group_id = int(message.command[1])
    except ValueError:
        return await message.reply_text("ɪɴᴠᴀʟɪᴅ ʟᴏɢɢᴇʀ ɪᴅ !!")

    if not str(group_id).startswith("-100"):
        return await message.reply_text("ɪɴᴠᴀʟɪᴅ ʟᴏɢɢᴇʀ ɪᴅ !!")

    try:
        await client.send_message(group_id, "ʙᴏᴛ ʟᴏɢɢɪɴɢ ᴇɴᴀʙʟᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!")
        # Fixed: Added await
        await clonebotdb.update_one(
            {"bot_id": bot_id},
            {"$set": {"logchannel": group_id}},
            upsert=True
        )
        return await message.reply_text(f"ʟᴏɢɢɪɴɢ ᴇɴᴀʙʟᴇᴅ ғᴏʀ `{group_id}`.")
    except Exception:
        return await message.reply_text(f"ʙᴏᴛ ᴄᴀɴ'ᴛ sᴇɴᴅ ᴍᴇssᴀɢᴇs ɪɴ ᴛʜɪs ɢʀᴏᴜᴘ!")
