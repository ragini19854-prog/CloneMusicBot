from pyrogram import filters, Client
from pyrogram.types import Message
from PritiMusic import app
from PritiMusic.misc import SUDOERS
from PritiMusic.utils.database import clonebotdb
from PritiMusic.utils.extraction import extract_user

# --- Command: Add Sudo ---
@Client.on_message(filters.command(["addsudo", "setsudo"]) & filters.group)
async def clone_add_sudo(client: Client, message: Message):
    bot_id = client.me.id
    user_id = message.from_user.id
    
    # 1. Fetch Bot Data
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return
        
    owner_id = clone_data.get("user_id")
    
    # 🔒 SILENT CHECK (Ignore non-owners)
    if user_id != owner_id:
        return 

    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("Usage: `/addsudo @User`")

    user = await extract_user(message)
    if not user:
        return await message.reply_text("❌ **User not found.**")

    if user.id == owner_id:
        return await message.reply_text("⚠️ **You are already the Owner.**")
    
    current_sudoers = clone_data.get("sudoers", [])
    
    if user.id in current_sudoers:
        return await message.reply_text(f"✅ {user.mention} **is already a Bot Admin.**")
    
    # Update Database
    await clonebotdb.update_one(
        {"bot_id": bot_id},
        {"$push": {"sudoers": user.id}}
    )
    
    await message.reply_text(f"✅ {user.mention} **has been promoted to Bot Admin!**")


# --- Command: Remove Sudo ---
@Client.on_message(filters.command(["delsudo", "rmsudo"]) & filters.group)
async def clone_del_sudo(client: Client, message: Message):
    bot_id = client.me.id
    user_id = message.from_user.id
    
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return
        
    owner_id = clone_data.get("user_id")
    
    # 🔒 SILENT CHECK
    if user_id != owner_id:
        return 

    if not message.reply_to_message and len(message.command) != 2:
        return await message.reply_text("Usage: `/delsudo @User`")

    user = await extract_user(message)
    if not user:
        return await message.reply_text("❌ **User not found.**")

    current_sudoers = clone_data.get("sudoers", [])
    
    if user.id not in current_sudoers:
        return await message.reply_text("⚠️ **This user is not in the Admin list.**")
    
    # Update Database
    await clonebotdb.update_one(
        {"bot_id": bot_id},
        {"$pull": {"sudoers": user.id}}
    )
    
    await message.reply_text(f"✅ {user.mention} **has been removed from Admin list.**")


# --- Command: Delete All Sudo ---
@Client.on_message(filters.command(["delallsudo", "rmallsudo"]) & filters.group)
async def clone_del_all_sudo(client: Client, message: Message):
    bot_id = client.me.id
    user_id = message.from_user.id
    
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return
        
    owner_id = clone_data.get("user_id")
    
    # 🔒 SILENT CHECK
    if user_id != owner_id:
        return 

    await clonebotdb.update_one(
        {"bot_id": bot_id},
        {"$set": {"sudoers": []}}
    )
    
    await message.reply_text("✅ **All Bot Admins have been removed successfully.**")


# --- Command: List Sudo ---
@Client.on_message(filters.command(["sudolist", "sudoers", "adminlist"]) & filters.group)
async def clone_sudo_list(client: Client, message: Message):
    bot_id = client.me.id
    user_id = message.from_user.id
    
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return
    
    # Optional: If you want ONLY the owner to see the list, uncomment below:
    # if user_id != clone_data.get("user_id"):
    #     return

    sudoers = clone_data.get("sudoers", [])
    
    try:
        owner_obj = await client.get_users(clone_data.get("user_id"))
        owner_name = owner_obj.mention
    except:
        owner_name = "Unknown Owner"

    text = f"👑 **Bot Owner:** {owner_name}\n\n"
    
    if not sudoers:
        text += "❌ **No Admins assigned yet.**"
    else:
        text += "👮 **Bot Admins:**\n"
        for user_id in sudoers:
            try:
                user = await client.get_users(user_id)
                text += f"➤ {user.mention}\n"
            except:
                text += f"➤ User ID: `{user_id}`\n"

    await message.reply_text(text)