from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from MadaraMusic import app
from MadaraMusic.misc import SUDOERS, db
from MadaraMusic.utils.database import (
    get_authuser_names,
    get_cmode,
    get_lang,
    get_upvote_count,
    is_active_chat,
    is_maintenance,
    is_nonadmin_chat,
    is_skipmode,
    clonebotdb, # ✅ Database Import
)
from config import SUPPORT_CHAT, adminlist, confirmer
from strings import get_string

# ✅ FIX: Ab formatters ko Cplugin wale folder se import kiya hai
from MadaraMusic.cplugin.utils.formatters import int_to_alpha

# --- HELPER: Clone Admin Checker ---
async def is_clone_admin(bot_id, user_id):
    """
    Check karega ki user Clone Bot ka Owner ya Sudo hai ya nahi.
    """
    try:
        clone_data = await clonebotdb.find_one({"bot_id": bot_id})
        if clone_data:
            # 1. Check Owner
            if user_id == clone_data.get("user_id"):
                return True
            # 2. Check Sudo List
            if "sudoers" in clone_data and user_id in clone_data["sudoers"]:
                return True
    except:
        pass
    return False


def AdminRightsCheck(mystic):
    async def wrapper(client, message):
        # 1. Maintenance Check
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} is under maintenance, visit <a href={SUPPORT_CHAT}>Support Chat</a> for reason.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        # 2. Check Anonymous Admin
        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to fix?",
                            callback_data="MadaramousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["general_3"], reply_markup=upl)

        # 3. Check Command Mode
        if message.command[0][0] == "c":
            chat_id = await get_cmode(message.chat.id)
            if chat_id is None:
                return await message.reply_text(_["setting_7"])
            try:
                await app.get_chat(chat_id)
            except:
                return await message.reply_text(_["cplay_4"])
        else:
            chat_id = message.chat.id

        # 4. Check Active Chat
        if not await is_active_chat(chat_id):
            return await message.reply_text(_["general_5"])

        # 5. Permission Check Logic
        is_non_admin = await is_nonadmin_chat(message.chat.id)
        if not is_non_admin:
            
            # ✅ CHECK CLONE OWNER / SUDO FIRST
            is_clone_auth = await is_clone_admin(client.me.id, message.from_user.id)
            
            if message.from_user.id not in SUDOERS and not is_clone_auth:
                admins = adminlist.get(message.chat.id)
                if not admins:
                    return await message.reply_text(_["admin_13"])
                else:
                    if message.from_user.id not in admins:
                        if await is_skipmode(message.chat.id):
                            upvote = await get_upvote_count(chat_id)
                            text = f"""<b>Admin Rights Needed</b>

Refresh Admin Cache via: /reload

» {upvote} votes needed for performing this action."""

                            command = message.command[0]
                            if command[0] == "c":
                                command = command[1:]
                            if command == "speed":
                                return await message.reply_text(_["admin_14"])
                            MODE = command.title()
                            upl = InlineKeyboardMarkup(
                                [
                                    [
                                        InlineKeyboardButton(
                                            text="Vote",
                                            callback_data=f"ADMIN UpVote|{chat_id}_{MODE}",
                                        ),
                                    ]
                                ]
                            )
                            if chat_id not in confirmer:
                                confirmer[chat_id] = {}
                            try:
                                vidid = db[chat_id][0]["vidid"]
                                file = db[chat_id][0]["file"]
                            except:
                                return await message.reply_text(_["admin_14"])
                            senn = await message.reply_text(text, reply_markup=upl)
                            confirmer[chat_id][senn.id] = {
                                "vidid": vidid,
                                "file": file,
                            }
                            return
                        else:
                            return await message.reply_text(_["admin_14"])

        return await mystic(client, message, _, chat_id)

    return wrapper


def AdminActual(mystic):
    async def wrapper(client, message):
        if await is_maintenance() is False:
            if message.from_user.id not in SUDOERS:
                return await message.reply_text(
                    text=f"{app.mention} is under maintenance, visit <a href={SUPPORT_CHAT}>Support Chat</a> for reason.",
                    disable_web_page_preview=True,
                )

        try:
            await message.delete()
        except:
            pass

        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if message.sender_chat:
            upl = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="How to fix?",
                            callback_data="MadaramousAdmin",
                        ),
                    ]
                ]
            )
            return await message.reply_text(_["general_3"], reply_markup=upl)

        # ✅ Check Clone Admin
        is_clone_auth = await is_clone_admin(client.me.id, message.from_user.id)

        if message.from_user.id not in SUDOERS and not is_clone_auth:
            try:
                member = (
                    await app.get_chat_member(message.chat.id, message.from_user.id)
                ).privileges
            except:
                return
            if not member.can_manage_video_chats:
                return await message.reply(_["general_4"])

        return await mystic(client, message, _)

    return wrapper


def ActualAdminCB(mystic):
    async def wrapper(client, CallbackQuery):
        if await is_maintenance() is False:
            if CallbackQuery.from_user.id not in SUDOERS:
                return await CallbackQuery.answer(
                    f"{app.mention} is under maintenance, visit Support Chat for reason.",
                    show_alert=True,
                )
        try:
            language = await get_lang(CallbackQuery.message.chat.id)
            _ = get_string(language)
        except:
            _ = get_string("en")

        if CallbackQuery.message.chat.type == ChatType.PRIVATE:
            return await mystic(client, CallbackQuery, _)

        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            try:
                a = (
                    await app.get_chat_member(
                        CallbackQuery.message.chat.id,
                        CallbackQuery.from_user.id,
                    )
                ).privileges
            except:
                return await CallbackQuery.answer(_["general_4"], show_alert=True)
            
            # ✅ Check Clone Admin
            is_clone_auth = await is_clone_admin(client.me.id, CallbackQuery.from_user.id)

            if not a.can_manage_video_chats and not is_clone_auth:
                if CallbackQuery.from_user.id not in SUDOERS:
                    token = await int_to_alpha(CallbackQuery.from_user.id)
                    _check = await get_authuser_names(CallbackQuery.from_user.id)
                    if token not in _check:
                        try:
                            return await CallbackQuery.answer(
                                _["general_4"],
                                show_alert=True,
                            )
                        except:
                            return
        return await mystic(client, CallbackQuery, _)

    return wrapper
