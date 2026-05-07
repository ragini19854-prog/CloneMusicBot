import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    PeerFlood, 
    UserPrivacyRestricted, 
    UserChannelsTooMuch,
    FloodWait,
    UserAlreadyParticipant
)
from PritiMusic import app
from PritiMusic.misc import SUDOERS  # ✅ Correct Import
from PritiMusic.utils.database import clonebotdb, get_assistant
from config import API_ID, API_HASH

# --- CONFIGURATION ---
DELAY_PER_ADD = 10     # Delay to prevent ban (Seconds)
HISTORY_LIMIT = 300    # How many messages to scan in hidden groups

# ✅ FIX: Removed filters.user() wrapper because SUDOERS is likely already a filter
@app.on_message(filters.command(["gadd", "gscrape"]) & SUDOERS)
async def global_scraper(client: Client, message: Message):
    # 1. Check Input
    if len(message.command) < 4:
        return await message.reply_text(
            "ℹ️ **Global Multi-Scraper Tool** (Owner Only)\n\n"
            "**Usage:** `/gadd [Source] [Target] [Amount]`\n"
            "**Example:** `/gadd @OldGroup @NewGroup 50`\n"
            "✨ _Hidden Members bhi scan kar lega._"
        )

    source_link = message.command[1]
    target_link = message.command[2]
    
    try:
        limit = int(message.command[3])
    except:
        return await message.reply_text("❌ **Amount number me likho!**")

    msg = await message.reply_text("🔄 **Initializing Assistants...**")

    # 2. Get All Connected Sessions
    sessions = []
    async for bot_data in clonebotdb.find({"session_string": {"$exists": True}}):
        if bot_data.get("session_string"):
            sessions.append(bot_data["session_string"])

    if not sessions:
        return await msg.edit_text("❌ **No Connected Clones Found!**")

    num_clones = len(sessions)
    await msg.edit_text(f"✅ **Found {num_clones} Clones.**\n♻️ Scraping Members...")

    # 3. Scrape Members (Using Main Assistant)
    scraper = await get_assistant(message.chat.id)
    members_to_add = []
    
    try:
        # Resolve Chat
        try:
            if "+" in source_link:
                chat = await scraper.join_chat(source_link)
                source_id = chat.id
            else:
                chat = await scraper.get_chat(source_link)
                source_id = chat.id
        except Exception as e:
            return await msg.edit_text(f"❌ **Source Access Error:** `{e}`")

        # Method A: Standard List
        try:
            async for member in scraper.get_chat_members(source_id, limit=limit + 20):
                if not member.user.is_bot and not member.user.is_deleted:
                    members_to_add.append(member.user.id)
                    if len(members_to_add) >= limit: break
        except:
            pass 
        
        # Method B: History Scan (If Hidden)
        if not members_to_add:
            await msg.edit_text("⚠️ **Hidden Members Detected!**\n🔄 Scanning Chat History...")
            async for m in scraper.get_chat_history(source_id, limit=HISTORY_LIMIT):
                if len(members_to_add) >= limit: break
                if m.from_user and not m.from_user.is_bot:
                    if m.from_user.id not in members_to_add:
                        members_to_add.append(m.from_user.id)

    except Exception as e:
        return await msg.edit_text(f"❌ **Scraping Failed:** `{e}`")

    if not members_to_add:
        return await msg.edit_text("❌ **Koi Members nahi mile.**")

    # 4. Distribute Work
    chunks = [members_to_add[i::num_clones] for i in range(num_clones)]
    
    await msg.edit_text(
        f"🚀 **Starting Transfer!**\n"
        f"👥 **Members:** {len(members_to_add)}\n"
        f"🤖 **Workers:** {num_clones}\n"
        f"⏳ **Target:** {target_link}"
    )

    # 5. Worker Function
    async def run_worker(session, users, wid):
        added = 0
        try:
            cli = Client(f"w_{wid}", api_id=API_ID, api_hash=API_HASH, session_string=session, no_updates=True, in_memory=True)
            await cli.start()
            
            # Join Target
            target_chat_id = None
            try:
                chat = await cli.join_chat(target_link)
                target_chat_id = chat.id
            except UserAlreadyParticipant:
                chat = await cli.get_chat(target_link)
                target_chat_id = chat.id
            except Exception:
                 # Try getting without join (Public)
                try:
                    chat = await cli.get_chat(target_link)
                    target_chat_id = chat.id
                except:
                    await cli.stop()
                    return 0

            for uid in users:
                try:
                    await cli.add_chat_members(target_chat_id, uid)
                    added += 1
                    await asyncio.sleep(DELAY_PER_ADD)
                except FloodWait as e:
                    await asyncio.sleep(e.value + 5)
                except (PeerFlood, UserPrivacyRestricted, UserChannelsTooMuch):
                    pass
                except:
                    pass
            
            await cli.stop()
            return added
        except:
            return 0

    # 6. Execute
    tasks = [run_worker(sessions[i], chunks[i], i) for i in range(num_clones) if i < len(chunks)]
    results = await asyncio.gather(*tasks)
    
    await message.reply_text(
        f"🏁 **Completed!**\n✅ **Total Added:** {sum(results)}\n🤖 **Clones Used:** {num_clones}"
    )