import random 
from pyrogram.types import InlineKeyboardButton
import config
from PritiMusic import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["SO_B_1"], 
                url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text="ᴄʟᴏɴᴇ", callback_data="clone_page")
        ],
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="support_page"),
            InlineKeyboardButton(text=" sᴏᴜʀᴄᴇ", callback_data="gib_source")
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper")
        ],
    ]
    return buttons

def support_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")
        ]
    ]
    return buttons

def about_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID),
            InlineKeyboardButton(text=_["S_B_11"], url=config.GITHUB),
        ],
        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT)
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper")
        ]
    ]
    return buttons
