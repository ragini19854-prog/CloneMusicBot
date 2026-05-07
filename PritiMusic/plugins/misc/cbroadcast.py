import asyncio
from pyrogram import filters, Client
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait, RPCError, PeerIdInvalid, UserIsBlocked, InputUserDeactivated, AuthKeyUnregistered

from PritiMusic import app
from PritiMusic.misc import SUDOERS
from PritiMusic.utils.database.clonedb import (
    get_all_clones, 
    get_served_chats_clone, 
    get_served_users_clone,
    get_clonebot_owner
)
from config import API_ID, API_HASH

# Global Flag
IS_CBROADCASTING = False

@app.on_message(filters.command("stopcbroadcast") & SUDOERS)
async def stop_clone_broadcast(client, message):
    global IS_CBROADCASTING
    if not IS_CBROADCASTING:
        return await message.reply_text("❌ **No Clone Broadcast is currently running.**")
    
    IS_CBROADCASTING = False
    await message.reply_text("🛑 **Stopping Broadcast...**\nProcess will halt after current bot.")


@app.on_message(filters.command("cbroadcast") & SUDOERS)
async def clone_broadcast_handler(client, message):
    global IS_CBROADCASTING
    
    if IS_CBROADCASTING:
        return await message.reply_text("⚠️ **Broadcast already running!** Stop it first.")

    # --- COMMAND PARSING ---
    if message.reply_to_message:
        query = message.reply_to_message.text or message.reply_to_message.caption
    else:
        if len(message.command) < 2:
            return await message.reply_text(
                "<b>📣 Clone Broadcast Manager</b>\n\n"
                "<b>Usage:</b> `/cbroadcast [Message] [Flags]`\n"
                "<b>Flags:</b> `-owner`, `-user`, `-group`, `-all`, `-pin`"
            )
        query = message.text.split(None, 1)[1]

    pin = "-pin" in message.text
    send_owners = "-owner" in message.text or "-all" in message.text
    send_users = "-user" in message.text or "-all" in message.text
    send_groups = "-group" in message.text or "-all" in message.text

    if not send_users and not send_groups and not send_owners:
        send_groups = True

    if query:
        for flag in ["-pin", "-owner", "-user", "-group", "-all"]:
            query = query.replace(flag, "")
        query = query.strip()

    if not query and not message.reply_to_message:
        return await message.reply_text("❌ **Message is empty!**")

    IS_CBROADCASTING = True
    status_msg = await message.reply_text("🔄 **Analyzing Clones...**")

    # --- FETCH CLONES ---
    all_clones_data = []
    try:
        async for c in get_all_clones():
            all_clones_data.append(c)
    except Exception as e:
        IS_CBROADCASTING = False
        return await status_msg.edit_text(f"❌ **DB Error:** {e}")

    total_clones = len(all_clones_data)
    if total_clones == 0:
        IS_CBROADCASTING = False
        return await status_msg.edit_text("❌ **No Clones Found.**")

    await status_msg.edit_text(f"🚀 **Targeting {total_clones} Clones...**")

    success_clones = 0
    failed_clones = 0
    total_sent = 0

    # --- MAIN LOOP ---
    for clone in all_clones_data:
        if not IS_CBROADCASTING: break

        token = clone.get('token')
        bot_id = clone.get('bot_id')
        username = clone.get('username', 'Unknown')

        if not token or not bot_id:
            failed_clones += 1
            continue

        # --- A. COLLECT TARGETS ---
        target_ids = set()

        # 1. Clone Owner
        if send_owners:
            try:
                owner = await get_clonebot_owner(bot_id)
                if owner:
                    target_ids.add(int(owner))
            except:
                pass

        # 2. Clone Users
        if send_users:
            try:
                users_list = await get_served_users_clone(bot_id)
                for u in users_list:
                    target_ids.add(int(u['user_id']))
            except:
                pass

        # 3. Clone Groups
        if send_groups:
            try:
                chats_list = await get_served_chats_clone(bot_id)
                for c in chats_list:
                    target_ids.add(int(c['chat_id']))
            except:
                pass

        # Skip if empty (Count as processed but not active)
        if not target_ids:
            continue

        # --- B. SEND MESSAGES ---
        try:
            async with Client(
                f":memory:",
                api_id=API_ID,
                api_hash=API_HASH,
                bot_token=token,
                in_memory=True,
                no_updates=True
            ) as clone_app:
                
                clone_sent_count = 0
                
                # Check if bot is alive
                try:
                    await clone_app.get_me()
                except (AuthKeyUnregistered, UserDeactivated):
                    failed_clones += 1
                    continue # Token expired

                for chat_id in target_ids:
                    if not IS_CBROADCASTING: break
                    
                    try:
                        if message.reply_to_message:
                            sent = await message.reply_to_message.copy(chat_id)
                        else:
                            sent = await clone_app.send_message(chat_id, query)
                        
                        if pin and sent and str(chat_id).startswith("-100"):
                            try:
                                await sent.pin(disable_notification=True)
                            except:
                                pass
                        
                        clone_sent_count += 1
                        total_sent += 1
                        await asyncio.sleep(0.2)
                    
                    except FloodWait as e:
                        await asyncio.sleep(int(e.value))
                    except Exception:
                        continue
                
                if clone_sent_count > 0:
                    success_clones += 1
                
        except Exception:
            failed_clones += 1
            continue

    # --- FINAL REPORT ---
    IS_CBROADCASTING = False
    await status_msg.edit_text(
        f"✅ **Broadcast Completed!**\n\n"
        f"🤖 **Total Clones:** {total_clones}\n"
        f"📢 **Active Sending:** {success_clones}\n"
        f"⚠️ **Failed/Revoked:** {failed_clones}\n"
        f"📨 **Messages Sent:** {total_sent}"
    )
