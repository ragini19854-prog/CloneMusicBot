from typing import Union

from pyrogram import enums
from pyrogram.types import InlineKeyboardButton


def setting_markup(_):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AU", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text=_["ST_B_3"], callback_data="LG", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_2"], callback_data="PM", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_4"], callback_data="VM", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons


def vote_mode_markup(_, current, mode: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text="Vσтιηg мσ∂є ➜", callback_data="VOTEANSWER", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(
                text=_["ST_B_5"] if mode == True else _["ST_B_6"],
                callback_data="VOMODECHANGE",
                style=enums.ButtonStyle.SUCCESS if mode == True else enums.ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(text="-2", callback_data="FERRARIUDTI M", style=enums.ButtonStyle.DANGER),
            InlineKeyboardButton(
                text=f"ᴄᴜʀʀᴇɴᴛ : {current}",
                callback_data="ANSWERVOMODE",
            ),
            InlineKeyboardButton(text="+2", callback_data="FERRARIUDTI A", style=enums.ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons


def auth_users_markup(_, status: Union[bool, str] = None):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_7"], callback_data="AUTHANSWER", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(
                text=_["ST_B_8"] if status == True else _["ST_B_9"],
                callback_data="AUTH",
                style=enums.ButtonStyle.SUCCESS if status == True else enums.ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_1"], callback_data="AUTHLIST", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons


def playmode_users_markup(
    _,
    Direct: Union[bool, str] = None,
    Group: Union[bool, str] = None,
    Playtype: Union[bool, str] = None,
):
    buttons = [
        [
            InlineKeyboardButton(text=_["ST_B_10"], callback_data="SEARCHANSWER", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(
                text=_["ST_B_11"] if Direct == True else _["ST_B_12"],
                callback_data="MODECHANGE",
                style=enums.ButtonStyle.SUCCESS if Direct == True else enums.ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_13"], callback_data="AUTHANSWER", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Group == True else _["ST_B_9"],
                callback_data="CHANNELMODECHANGE",
                style=enums.ButtonStyle.SUCCESS if Group == True else enums.ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(text=_["ST_B_14"], callback_data="PLAYTYPEANSWER", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(
                text=_["ST_B_8"] if Playtype == True else _["ST_B_9"],
                callback_data="PLAYTYPECHANGE",
                style=enums.ButtonStyle.SUCCESS if Playtype == True else enums.ButtonStyle.DANGER,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["BACK_BUTTON"],
                callback_data="settings_helper",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons
