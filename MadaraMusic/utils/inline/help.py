from typing import Union
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from MadaraMusic import app

def help_pannel(_, START: Union[bool, int] = None):
    first = [
        [
            InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_4"], callback_data="help_callback hb4", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_5"], callback_data="help_callback hb5", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_7"], callback_data="help_callback hb7", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback hb9", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_helper", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return InlineKeyboardMarkup(first)


def first_page(_, is_owner: bool = False):
    first = [
        [
            InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_3"], callback_data="help_callback hb3", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_11"], callback_data="help_callback hb11", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_8"], callback_data="help_callback hb8", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_6"], callback_data="help_callback hb6", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_13"], callback_data="help_callback hb13", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_12"], callback_data="help_callback hb12", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_9"], callback_data="help_callback cloghelp", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["H_B_10"], callback_data="help_callback hb10", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_14"], callback_data="help_callback hb14", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["H_B_15"], callback_data="help_callback hb15", style=enums.ButtonStyle.PRIMARY),
        ],
    ]

    if is_owner:
        first.append([
            InlineKeyboardButton(text="🛠 ᴄʟᴏɴᴇ ғᴇᴀᴛᴜʀᴇ", callback_data="help_callback chelp", style=enums.ButtonStyle.SUCCESS),
        ])

    first.append([
        InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settingsback_home", style=enums.ButtonStyle.PRIMARY),
    ])

    return InlineKeyboardMarkup(first)


def clone_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(text="ᴍᴀɴᴀɢᴇ", callback_data="help_callback clone_manage", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="sᴛᴀʀᴛ", callback_data="help_callback clone_start", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="ᴘɪɴɢ", callback_data="help_callback clone_ping", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="ᴘʟᴀʏ ᴍᴏᴅᴇ", callback_data="help_callback clone_play", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="ʟᴏɢɢᴇʀ", callback_data="help_callback clone_logger", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="ʙᴜᴛᴛᴏɴs & ʀᴇɴᴀᴍᴇ", callback_data="help_callback clone_buttons", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return InlineKeyboardMarkup(buttons)


def clone_back_markup(_):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="help_callback chelp",
                style=enums.ButtonStyle.PRIMARY,
            )
        ]]
    )


def help_back_markup(_):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_back_helper",
                style=enums.ButtonStyle.PRIMARY,
            )
        ]]
    )


def private_help_panel(_):
    return InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
                style=enums.ButtonStyle.PRIMARY,
            )
        ]]
    )
