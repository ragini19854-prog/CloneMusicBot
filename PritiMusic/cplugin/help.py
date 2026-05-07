import random
from typing import Union
from pyrogram import filters, types, Client
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram.errors import MessageNotModified

from PritiMusic import app
from PritiMusic.utils.inline.help import help_back_markup, private_help_panel, clone_help_panel, clone_back_markup
from PritiMusic.utils import first_page
from PritiMusic.utils import help_pannel
from PritiMusic.utils.database import get_lang
from PritiMusic.utils.decorators.language import LanguageStart, languageCB
from config import BANNED_USERS, HELP_IMG_URL, SUPPORT_CHAT
from strings import get_string, helpers
from PritiMusic.utils.stuffs.helper import Helper
from PritiMusic.utils.database.clonedb import get_owner_id_from_db, get_cloned_support_chat, get_cloned_support_channel

# ✅ Helper to safe get Random Image
def get_random_help_img():
    if HELP_IMG_URL:
        if isinstance(HELP_IMG_URL, list):
            return random.choice(HELP_IMG_URL)
        return HELP_IMG_URL
    return "https://telegra.ph/file/2e3d368e77c449c287430.jpg" # Fallback

@Client.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@Client.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    bot = await client.get_me()
    
    C_BOT_OWNER_ID = await get_owner_id_from_db(bot.id)
    
    C_BOT_SUPPORT_CHAT = await get_cloned_support_chat(bot.id)
    C_SUPPORT_CHAT = f"https://t.me/{C_BOT_SUPPORT_CHAT}"
    
    is_callback = isinstance(update, types.CallbackQuery)
    
    user_id = update.from_user.id
    is_owner = (user_id == C_BOT_OWNER_ID)

    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        
        keyboard = first_page(_, is_owner)
        
        try:
            await update.edit_message_text(
                _["help_1"].format(C_SUPPORT_CHAT), reply_markup=keyboard
            )
        except MessageNotModified:
            pass
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        
        keyboard = first_page(_, is_owner)
        
        # ✅ Random Photo + Spoiler Logic
        await update.reply_photo(
            photo=get_random_help_img(),
            caption=_["help_1"].format(C_SUPPORT_CHAT),
            reply_markup=keyboard,
            has_spoiler=True # ✨ Spoiler Added
        )


@Client.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


@Client.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    
    keyboard = help_back_markup(_)
    clone_back_kb = clone_back_markup(_)
    
    try:
        if cb == "hb1":
            await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
        elif cb == "hb2":
            await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
        elif cb == "hb3":
            await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
        elif cb == "hb4":
            await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
        elif cb == "hb5":
            await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
        elif cb == "hb6":
            await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
        elif cb == "hb7":
            await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
        elif cb == "hb8":
            await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
        elif cb == "hb9":
            await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
        elif cb == "hb10":
            await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
        elif cb == "hb11":
            await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
        elif cb == "hb12":
            await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
        elif cb == "hb13":
            await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
        elif cb == "hb14":
            await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
        elif cb == "hb15":
            await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
        
        # --- CLONE OWNER MENU ---
        elif cb == "chelp":
            clone_kb = clone_help_panel(_)
            await CallbackQuery.edit_message_text(helpers.CLONE_HELP_MENU, reply_markup=clone_kb)

        elif cb == "clone_manage":
            await CallbackQuery.edit_message_text(helpers.CLONE_MANAGE, reply_markup=clone_back_kb)

        elif cb == "clone_start":
            await CallbackQuery.edit_message_text(helpers.CLONE_START, reply_markup=clone_back_kb)
        
        elif cb == "clone_ping":
            await CallbackQuery.edit_message_text(helpers.CLONE_PING, reply_markup=clone_back_kb)

        elif cb == "clone_buttons":
            # Merged Button & Rename Help
            await CallbackQuery.edit_message_text(helpers.CLONE_BUTTONS, reply_markup=clone_back_kb)

        # ✅ Added New Play Mode Help
        elif cb == "clone_play":
            await CallbackQuery.edit_message_text(helpers.CLONE_PLAY_MODE, reply_markup=clone_back_kb)

        elif cb == "clone_logger":
            await CallbackQuery.edit_message_text(helpers.CLONE_LOGGER, reply_markup=clone_back_kb)
            
    except MessageNotModified:
        pass
    except Exception as e:
        print(f"Help Menu Error: {e}")
