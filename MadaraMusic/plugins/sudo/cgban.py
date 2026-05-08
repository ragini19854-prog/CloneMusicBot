import asyncio
import os
import random
from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserAdminInvalid, PeerIdInvalid, UserIsBlocked, InputUserDeactivated, AuthKeyUnregistered, UserDeactivated
from pyrogram.types import Message

from MadaraMusic import app
from MadaraMusic.misc import SUDOERS
from MadaraMusic.utils.database.clonedb import (
    get_all_clones, 
    get_served_chats_clone
)
from MadaraMusic.utils.decorators.language import language
from MadaraMusic.utils.extraction import extract_user
# ✅ Change: LOGGER_ID import kiya hai
from config import API_ID, API_HASH, START_IMG_URL, LOGGER_ID 

# Global Flag to Stop Process
IS_CGBAN_RUNNING = False

# ✅ Helper for Random Image
def get_random_cgban_img():
    if START_IMG_URL:
        if isinstance(START_IMG_URL, list):
            return random.choice(START_IMG_URL)
        return START_IMG_URL
    return "https://telegra.ph/file/2e3d368e77c449c287430.jpg"

@app.on_message(filters.command(["stopcgban", "stopclonegban"]) & SUDOERS)
async def stop_cgban_process(client, message):
    global IS_CGBAN_RUNNING
    if not IS_CGBAN_RUNNING:
        return await message.reply_text("❌ **No Clone Global Ban is running.**")
    
    IS_CGBAN_RUNNING = False
    await message.reply_text("🛑 **Stopping Clone Gban...**\nProcess will halt after current batch.")

# --- Helper: Async Ban Executor for Single Clone ---
async def execute_ban_via_clone(token, bot_id, user_id, unban=False):
    groups_affected = 0
    status = "FAILED"
    
    try:
        # Fetch chats where this clone is present
        chats = await get_served_chats_clone(bot_id)
        if not chats:
            return 0, "NO_CHATS"

        async with Client(
            f"cgban_{bot_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=token,
            in_memory=True,
            no_updates=True
        ) as clone_app:
            
            for chat in chats:
                chat_id = int(chat['chat_id'])
                try:
                    if unban:
                        await clone_app.unban_chat_member(chat_id, user_id)
                    else:
                        await clone_app.ban_chat_member(chat_id, user_id)
                    groups_affected += 1
                    await asyncio.sleep(0.1) # Micro sleep
                except (UserAdminInvalid, PeerIdInvalid):
                    continue 
                except FloodWait as e:
                    await asyncio.sleep(int(e.value))
                except Exception:
                    continue
            
            status = "SUCCESS"
            
    except (AuthKeyUnregistered, UserDeactivated):
        status = "TOKEN_EXPIRED"
    except Exception:
        status = "ERROR"
        
    return groups_affected, status

@app.on_message(filters.command(["cgban", "clonegban"]) & SUDOERS)
@language
async def clone_global_ban_all(client, message: Message, _):
    global IS_CGBAN_RUNNING
    
    if IS_CGBAN_RUNNING:
        return await message.reply_text("⚠️ **A process is already running!** Stop it first.")

    if not message.reply_to_message:
        if len(message.command) < 2:
            return await message.reply_text("Usage: `/cgban @User [Reason]`")
    
    user = await extract_user(message)
    
    # --- Reason Extraction Logic ---
    reason = "No reason provided."
    if len(message.command) > 2:
        reason = message.text.split(None, 2)[2]
    elif message.reply_to_message and len(message.command) > 1:
        reason = message.text.split(None, 1)[1]
    
    # --- Safety Checks ---
    if user.id == message.from_user.id:
        return await message.reply_text(_["gban_1"])
    elif user.id in SUDOERS:
        return await message.reply_text(_["gban_3"])

    IS_CGBAN_RUNNING = True
    
    mystic = await message.reply_photo(
        photo=get_random_cgban_img(),
        caption=f"☢️ **INITIATING CLONE GLOBAL BAN**\n\n**Target:** {user.mention}\n**ID:** `{user.id}`\n**Reason:** `{reason}`\n\n🔄 **Scanning Clones Network...**",
        has_spoiler=True
    )

    # --- Fetch Clones ---
    all_clones = []
    async for c in get_all_clones():
        all_clones.append(c)
        
    if not all_clones:
        IS_CGBAN_RUNNING = False
        return await mystic.edit_text("❌ **No Clones Found in Database.**")

    await mystic.edit_caption(f"☢️ **CLONE GBAN RUNNING**\n\n**Target:** {user.mention}\n**Reason:** `{reason}`\n**Clones:** {len(all_clones)}\n⚡ **Executing Bans...**")

    # --- Execution Loop ---
    total_clones = len(all_clones)
    active_clones_used = 0
    total_groups_banned = 0
    
    REPORT_LOGS = [f"CLONE GBAN REPORT\nTarget: {user.id}\nReason: {reason}\n"]

    BATCH_SIZE = 10 
    
    for i in range(0, total_clones, BATCH_SIZE):
        if not IS_CGBAN_RUNNING: break
        
        batch = all_clones[i:i + BATCH_SIZE]
        tasks = []
        
        for clone in batch:
            token = clone.get('token')
            bot_id = clone.get('bot_id')
            bot_user = clone.get('username', 'Unknown')
            
            if token and bot_id:
                task = asyncio.create_task(execute_ban_via_clone(token, bot_id, user.id, unban=False))
                tasks.append((task, bot_user))

        for task, bot_user in tasks:
            affected, status = await task
            if status == "SUCCESS" or status == "NO_CHATS":
                active_clones_used += 1
            
            if affected > 0:
                total_groups_banned += affected
                REPORT_LOGS.append(f"@{bot_user}: Banned in {affected} chats.")
            elif status == "TOKEN_EXPIRED":
                REPORT_LOGS.append(f"@{bot_user}: FAILED (Token Expired)")

        if i % 20 == 0:
            try:
                await mystic.edit_caption(
                    f"☢️ **CLONE GBAN PROGRESS**\n\n"
                    f"🤖 **Clones Checked:** {i}/{total_clones}\n"
                    f"🚫 **Groups Affected:** {total_groups_banned}"
                )
            except:
                pass

    IS_CGBAN_RUNNING = False
    
    # --- Final Report ---
    final_text = (
        f"✅ **Clone Gban Completed!**\n\n"
        f"👤 **Target:** {user.mention}\n"
        f"📝 **Reason:** `{reason}`\n"
        f"🤖 **Clones Active:** {active_clones_used}/{total_clones}\n"
        f"🚫 **Total Groups Banned:** {total_groups_banned}\n"
    )
    
    await mystic.edit_caption(final_text)
    
    if len(REPORT_LOGS) > 1:
        file_name = f"cgban_{user.id}.txt"
        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(REPORT_LOGS))
        try:
            await message.reply_document(file_name, caption=f"📊 **Ban Report: {reason}**")
            os.remove(file_name)
        except:
            pass

    # ✅ Log to LOGGER_ID
    if LOGGER_ID:
        try:
            await app.send_message(
                LOGGER_ID,
                f"**☢️ #CLONE_GLOBAL_BAN**\n\n**Admin:** {message.from_user.mention}\n**Target:** {user.mention} [`{user.id}`]\n**Reason:** `{reason}`\n**Impact:** {total_groups_banned} groups."
            )
        except:
            pass


@app.on_message(filters.command(["cungban", "cloneungban"]) & SUDOERS)
@language
async def clone_global_unban_all(client, message: Message, _):
    global IS_CGBAN_RUNNING
    
    if IS_CGBAN_RUNNING:
        return await message.reply_text("⚠️ **A process is already running!**")

    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    IS_CGBAN_RUNNING = True
    
    mystic = await message.reply_photo(
        photo=get_random_cgban_img(),
        caption=f"🕊️ **INITIATING CLONE GLOBAL UNBAN**\n\n**Target:** {user.mention}\n🔄 **Scanning Network...**",
        has_spoiler=True
    )

    all_clones = []
    async for c in get_all_clones():
        all_clones.append(c)

    total_groups_unbanned = 0
    BATCH_SIZE = 10
    
    for i in range(0, len(all_clones), BATCH_SIZE):
        if not IS_CGBAN_RUNNING: break
        batch = all_clones[i:i + BATCH_SIZE]
        tasks = []
        
        for clone in batch:
            token = clone.get('token')
            bot_id = clone.get('bot_id')
            if token and bot_id:
                task = asyncio.create_task(execute_ban_via_clone(token, bot_id, user.id, unban=True))
                tasks.append(task)

        for task in tasks:
            affected, status = await task
            total_groups_unbanned += affected

    IS_CGBAN_RUNNING = False
    
    await mystic.edit_caption(
        f"✅ **Clone Unban Completed!**\n\n"
        f"👤 **Target:** {user.mention}\n"
        f"🕊️ **Groups Unbanned:** {total_groups_unbanned}"
    )