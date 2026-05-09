from pyrogram import enums
from pyrogram.types import InlineKeyboardButton
import config
from MadaraMusic import app

def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["SO_B_1"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT, style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons

def private_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            )
        ],
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID, style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="ᴄʟᴏɴᴇ", callback_data="clone_page", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="sᴜᴘᴘᴏʀᴛ", callback_data="support_page", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="sᴏᴜʀᴄᴇ", callback_data="gib_source", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons

def support_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT, style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL, style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper", style=enums.ButtonStyle.PRIMARY),
        ]
    ]
    return buttons

def about_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["S_B_5"], user_id=config.OWNER_ID, style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["S_B_11"], url=config.GITHUB, style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["S_B_6"], url=config.SUPPORT_CHANNEL, style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT, style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper", style=enums.ButtonStyle.PRIMARY),
        ]
    ]
    return buttons
