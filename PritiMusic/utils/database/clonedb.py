from PritiMusic.core.mongo import mongodb
from typing import Dict, List, Union

# ==========================================
#           MONGODB COLLECTIONS
# ==========================================
cloneownerdb = mongodb.cloneownerdb
clonebotnamedb = mongodb.clonebotnamedb
chatsdbc = mongodb.chatsc
usersdbc = mongodb.tgusersdbc
clonebotdb = mongodb.clonebotdb
clone_custom_db = mongodb.clone_custom_settings

# ==========================================
#        GLOBAL CLONE MANAGEMENT
# ==========================================

def get_all_clones():
    """Returns cursor for all clone bots."""
    return clonebotdb.find()

async def save_clonebot_owner(bot_id, user_id):
    """Saves the owner ID of a clone bot."""
    await cloneownerdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"user_id": user_id}},
        upsert=True
    )

async def get_clonebot_owner(bot_id):
    """Retrieves the owner ID of a clone bot (From Owner DB)."""
    query = {"bot_id": {"$in": [int(bot_id), str(bot_id)]}}
    result = await cloneownerdb.find_one(query)
    if result:
        return result.get("user_id")
    return False

async def save_clonebot_username(bot_id, user_name):
    """Saves the username of a clone bot."""
    await clonebotnamedb.update_one(
        {"bot_id": bot_id},
        {"$set": {"user_name": user_name}},
        upsert=True
    )

async def get_clonebot_username(bot_id):
    """Retrieves the username of a clone bot."""
    result = await clonebotnamedb.find_one({"bot_id": bot_id})
    if result:
        return result.get("user_name")
    return False

async def get_owner_id_from_db(bot_id):
    """Retrieves owner ID directly from the main clone DB."""
    bot_data = await clonebotdb.find_one({"bot_id": bot_id})
    if bot_data:
        return bot_data.get("user_id")
    return None

async def get_cloned_support_chat(bot_id: int) -> str:
    """Retrieves the support chat link for a clone bot."""
    bot_details = await clonebotdb.find_one({"bot_id": bot_id})
    if bot_details:
        return bot_details.get("support", "No support chat set.")
    return "No support chat set."

async def get_cloned_support_channel(bot_id: int) -> str:
    """Retrieves the support channel link for a clone bot."""
    bot_details = await clonebotdb.find_one({"bot_id": bot_id})
    if bot_details:
        return bot_details.get("channel", "No channel set.")
    return "No channel set."

async def has_user_cloned_any_bot(user_id: int) -> bool:
    """Checks if a user has created any clone bot."""
    cloned_bot = await clonebotdb.find_one({"user_id": user_id})
    if cloned_bot:
        return True
    return False

# ==========================================
#      CUSTOMIZATION (PLAY/SEARCH)
# ==========================================

async def set_clone_search_type(bot_id, type_name, content):
    """
    Saves the search message preference.
    type_name: 'text', 'sticker', 'animation', 'video', 'photo'
    content: The text message or file_id (supports ||| list)
    """
    await clone_custom_db.update_one(
        {"bot_id": bot_id},
        {"$set": {type_name: content}}, # Updates specific field
        upsert=True
    )

async def get_clone_search_type(bot_id, type_name):
    """Retrieves raw content for a specific type (used for append logic)."""
    data = await clone_custom_db.find_one({"bot_id": bot_id})
    if not data:
        return None
    return data.get(type_name)

async def get_clone_search_settings(bot_id):
    """
    Retrieves the HIGHEST PRIORITY search preference for Play Mode.
    Priority: Video > Photo > Animation > Sticker > Text
    Returns: (type_name, content)
    """
    data = await clone_custom_db.find_one({"bot_id": bot_id})
    if not data:
        return None, None
    
    # Priority Logic
    if data.get("video"):
        return "video", data.get("video")
    if data.get("photo"):
        return "photo", data.get("photo")
    if data.get("animation"):
        return "animation", data.get("animation")
    if data.get("sticker"):
        return "sticker", data.get("sticker")
    if data.get("text"):
        return "text", data.get("text")
        
    return None, None

async def delete_clone_search_type(bot_id):
    """Deletes ALL search mode settings (Reset to default)."""
    await clone_custom_db.update_one(
        {"bot_id": bot_id},
        {"$unset": {
            "video": "",
            "photo": "",
            "animation": "",
            "sticker": "",
            "text": ""
        }}
    )

# --- Stream Caption ---

async def set_clone_stream_caption(bot_id, caption):
    """Saves the custom stream caption."""
    await clone_custom_db.update_one(
        {"bot_id": bot_id},
        {"$set": {"stream_caption": caption}},
        upsert=True
    )

async def get_clone_stream_caption(bot_id):
    """Retrieves the custom stream caption."""
    data = await clone_custom_db.find_one({"bot_id": bot_id})
    if not data:
        return None
    return data.get("stream_caption")

async def delete_clone_stream_caption(bot_id):
    """Deletes the custom stream caption."""
    await clone_custom_db.update_one(
        {"bot_id": bot_id},
        {"$unset": {"stream_caption": ""}}
    )

# ==========================================
#        BROADCAST HELPERS
# ==========================================

async def get_served_chats_clone(bot_id):
    """Fetches all chats served by a specific clone bot."""
    served_chats = []
    # Query supports both int and str to be safe
    query = {"bot_id": {"$in": [int(bot_id), str(bot_id)]}}
    async for chat in chatsdbc.find(query):
        served_chats.append(chat)
    return served_chats

async def get_served_users_clone(bot_id):
    """Fetches all users served by a specific clone bot."""
    served_users = []
    # Query supports both int and str to be safe
    query = {"bot_id": {"$in": [int(bot_id), str(bot_id)]}}
    async for user in usersdbc.find(query):
        served_users.append(user)
    return served_users
