import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import (
    SessionPasswordNeeded, FloodWait,
    PhoneNumberInvalid, ApiIdInvalid,
    PhoneCodeInvalid, PhoneCodeExpired,
    UserDeactivated, AuthKeyUnregistered,
    PasswordHashInvalid
)
from PritiMusic.utils.database import clonebotdb
from config import API_ID, API_HASH, OWNER_ID

# ==========================================
# 1. CONNECT ASSISTANT (Phone + OTP)
# Command: /connect
# ==========================================
@Client.on_message(filters.command(["connect"]) & filters.private)
async def connect_assistant(client: Client, message: Message):
    bot_id = client.me.id
    user = message.from_user

    # 1. Verify Database (Async Fix)
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return await message.reply_text("❌ **Error:** Bot data not found in the database.")

    # 2. Access Check
    if clone_data["user_id"] != user.id and user.id != OWNER_ID:
        return await message.reply_text("❌ **Access Denied:** Only the bot owner can perform this action.")

    await message.reply_text(
        "⚡ **Connect Assistant**\n"
        "I will help you connect your account safely.\n\n"
        "🛑 Type `/cancel` anytime to stop."
    )

    # --- Step 1: Ask Phone Number ---
    try:
        phone_msg = await message.chat.ask(
            "📲 **Please send your Telegram Phone Number:**\n"
            "(Example: `+919876543210`)\n\n"
            "⚠️ **Don't forget the Country Code!**",
            timeout=300
        )
    except Exception:
        return await message.reply("❌ Time limit exceeded. Please try again.")

    if not phone_msg.text or phone_msg.text == "/cancel":
        return await message.reply("❌ Process Cancelled.")

    phone_number = phone_msg.text.strip()

    # --- Step 2: Create Temporary Client ---
    msg = await message.reply("🔄 **Connecting to Server...**")
    
    # Using in_memory=True to avoid creating session files
    temp_client = Client(
        name=f"connect_{bot_id}",
        api_id=API_ID,
        api_hash=API_HASH,
        in_memory=True
    )
    
    try:
        await temp_client.connect()
    except Exception as e:
        await msg.edit(f"❌ **Connection Failed:** `{str(e)}`")
        return

    # --- Step 3: Send OTP Code ---
    try:
        try:
            code = await temp_client.send_code(phone_number)
        except PhoneNumberInvalid:
            await msg.edit("❌ **Invalid Phone Number!** Please send in correct format (Ex: +91...).")
            return
        except ApiIdInvalid:
            await msg.edit("❌ **Internal Error:** API ID is invalid.")
            return
        except FloodWait as e:
            await msg.edit(f"❌ **FloodWait:** Please wait for {e.value} seconds before connecting.")
            return
        except Exception as e:
            await msg.edit(f"❌ **Error:** `{e}`")
            return

        await msg.delete()

        # --- Step 4: Ask for OTP ---
        try:
            otp_msg = await message.chat.ask(
                "📩 **OTP Sent!**\n\n"
                "Check your Telegram messages. Send the OTP code like this:\n"
                "Format: `1 2 3 4 5` (Space between each number)",
                timeout=300
            )
        except Exception:
            return await message.reply("❌ Time limit exceeded.")

        if not otp_msg.text or otp_msg.text == "/cancel":
            return await message.reply("❌ Process Cancelled.")

        otp = otp_msg.text.replace(" ", "").strip()

        # --- Step 5: Sign In ---
        try:
            await temp_client.sign_in(phone_number, code.phone_code_hash, otp)
        except PhoneCodeInvalid:
            await message.reply("❌ **Wrong OTP!** Please try again.")
            return
        except PhoneCodeExpired:
            await message.reply("❌ **OTP Expired.** Please try again.")
            return
        except SessionPasswordNeeded:
            # --- Step 6: Handle 2FA Password ---
            try:
                pwd_msg = await message.chat.ask(
                    "🔐 **Two-Step Verification:**\n\n"
                    "Your account is protected with a password. Please enter it below:",
                    timeout=300
                )
            except Exception:
                return await message.reply("❌ Time limit exceeded.")
            
            if not pwd_msg.text or pwd_msg.text == "/cancel":
                return await message.reply("❌ Process Cancelled.")
            
            try:
                await temp_client.check_password(password=pwd_msg.text)
            except PasswordHashInvalid:
                await message.reply("❌ **Wrong Password!** Connection failed.")
                return
            except Exception as e:
                await message.reply(f"❌ **Error:** `{str(e)}`")
                return
        except Exception as e:
            await message.reply(f"❌ **Error:** `{str(e)}`")
            return

        # --- Step 7: Export String & Connect ---
        await message.reply("🔄 **Connection Successful! Starting Assistant...**")
        
        try:
            # Stop old assistant if running
            if hasattr(client, "assistant") and client.assistant:
                try:
                    await client.assistant.stop()
                except:
                    pass
                try:
                    del client.assistant
                except:
                    pass

            string_session = await temp_client.export_session_string()
            
            # Send String to Saved Messages
            try:
                await temp_client.send_message(
                    "me", 
                    f"**Here is your Connected Session String:**\n\n`{string_session}`\n\n⚠️ _Do not share this with anyone!_"
                )
            except Exception:
                pass 

            # Save to Database (Async Fix)
            await clonebotdb.update_one(
                {"bot_id": bot_id},
                {"$set": {"session_string": string_session}}
            )

            # Connect Assistant
            new_assistant = Client(
                f"Ass_{bot_id}",
                api_id=API_ID,
                api_hash=API_HASH,
                session_string=string_session,
                no_updates=True,
                in_memory=True
            )
            await new_assistant.start()
            ass_info = await new_assistant.get_me()
            client.assistant = new_assistant

            await message.reply_text(
                f"🎉 **Connected Successfully!**\n\n"
                f"👤 **Assistant:** {ass_info.first_name}\n"
                f"🆔 **ID:** `{ass_info.id}`\n"
                f"📩 **Backup:** Session sent to your Saved Messages.\n\n"
                "🎸 **Now you can play music directly!**"
            )

        except Exception as e:
            await message.reply(f"❌ **Error Connecting:** `{str(e)}`")

    finally:
        if temp_client.is_connected:
            await temp_client.disconnect()


# ==========================================
# 2. MANUAL SET STRING (Paste String)
# Command: /setstring
# ==========================================
@Client.on_message(filters.command(["setstring", "setmode"]) & filters.private)
async def set_clone_session(client: Client, message: Message):
    bot_id = client.me.id
    user = message.from_user

    # 1. Verify Owner (Async Fix)
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return await message.reply_text("❌ **Error:** Bot data not found in database.")

    if clone_data["user_id"] != user.id and user.id != OWNER_ID:
        return await message.reply_text("❌ **Access Denied:** Only the owner can set the session.")

    if len(message.command) < 2:
        return await message.reply_text(
            "⚠️ **Usage:**\n`/setstring <Session_String>`\n\n"
            "❗ **Note:** Only **Pyrogram V2 Strings** are supported."
        )

    # Clean the string
    string_session = message.text.split(None, 1)[1].strip()
    msg = await message.reply_text("🔄 **Processing String...**")

    try:
        # 2. Stop Old Assistant
        if hasattr(client, "assistant") and client.assistant:
            try:
                await client.assistant.stop()
            except:
                pass
            try:
                del client.assistant
            except:
                pass

        # 3. Create and Start Assistant
        new_assistant = Client(
            f"Ass_{bot_id}",
            api_id=API_ID,
            api_hash=API_HASH,
            session_string=string_session,
            no_updates=True,
            in_memory=True
        )
        
        await new_assistant.start()
        ass_info = await new_assistant.get_me()

        # 4. Attach Assistant
        client.assistant = new_assistant

        # 5. Database Update (Async Fix)
        await clonebotdb.update_one(
            {"bot_id": bot_id},
            {"$set": {"session_string": string_session}}
        )
        
        await msg.edit(
            f"✅ **Connected Successfully!**\n\n"
            f"👤 **Assistant:** {ass_info.first_name}\n"
            f"🆔 **ID:** `{ass_info.id}`\n\n"
            "🎸 **Now you can play music!**"
        )

    except (UserDeactivated, AuthKeyUnregistered):
        await msg.edit("❌ **Invalid String:** This session has expired. Please connect again.")
    except Exception as e:
        await msg.edit(f"❌ **Error:** `{str(e)}`")


# ==========================================
# 3. DISCONNECT / REMOVE SESSION
# Command: /disconnect
# ==========================================
@Client.on_message(filters.command(["disconnect", "delstring"]) & filters.private)
async def disconnect_assistant(client: Client, message: Message):
    bot_id = client.me.id
    user = message.from_user

    # 1. Verify Owner (Async Fix)
    clone_data = await clonebotdb.find_one({"bot_id": bot_id})
    if not clone_data:
        return await message.reply_text("❌ **Error:** Bot data not found in database.")

    if clone_data["user_id"] != user.id and user.id != OWNER_ID:
        return await message.reply_text("❌ **Access Denied:** Only the owner can disconnect.")

    msg = await message.reply_text("🔄 **Disconnecting...**")

    try:
        # 2. Stop and Remove Running Assistant
        if hasattr(client, "assistant") and client.assistant:
            try:
                await client.assistant.stop()
            except:
                pass 
            try:
                del client.assistant
            except:
                pass

        # 3. Database Update ($unset) (Async Fix)
        await clonebotdb.update_one(
            {"bot_id": bot_id},
            {"$unset": {"session_string": 1}}
        )
        
        await msg.edit(
            "✅ **Disconnected Successfully!**\n\n"
            "Assistant has been removed."
        )

    except Exception as e:
        await msg.edit(f"❌ **Error:** `{str(e)}`")