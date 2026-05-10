import math
from config import SUPPORT_CHAT, OWNER_USERNAME
from pyrogram import enums
from pyrogram.types import InlineKeyboardButton
from MadaraMusic import app
import config
from MadaraMusic.utils.formatters import time_to_seconds


def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=enums.ButtonStyle.DANGER,
            )
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)

    if 0 < umm <= 10:
        bar = "◉—————————"
    elif 10 < umm < 20:
        bar = "—◉————————"
    elif 20 <= umm < 30:
        bar = "——◉———————"
    elif 30 <= umm < 40:
        bar = "———◉——————"
    elif 40 <= umm < 50:
        bar = "————◉—————"
    elif 50 <= umm < 60:
        bar = "—————◉————"
    elif 60 <= umm < 70:
        bar = "——————◉———"
    elif 70 <= umm < 80:
        bar = "———————◉——"
    elif 80 <= umm < 95:
        bar = "————————◉—"
    else:
        bar = "—————————◉"

    buttons = [
        [
            InlineKeyboardButton(
                text=f"{played} {bar} {dur}",
                callback_data="GetTimer",
            )
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ]
    ]
    return buttons


def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ]
    ]
    return buttons


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MadaraPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MadaraPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=enums.ButtonStyle.DANGER,
            ),
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"],
                callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {videoid}|{user_id}",
                style=enums.ButtonStyle.DANGER,
            ),
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁",
                callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"],
                callback_data=f"forceclose {query}|{user_id}",
                style=enums.ButtonStyle.DANGER,
            ),
            InlineKeyboardButton(
                text="▷",
                callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}",
                style=enums.ButtonStyle.PRIMARY,
            ),
        ],
    ]
    return buttons


def telegram_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text="Nєχт",
                callback_data=f"PanelMarkup None|{chat_id}",
                style=enums.ButtonStyle.PRIMARY,
            ),
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons


def queue_markup(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(text="II ραυѕє", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢ ѕтσρ", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
            InlineKeyboardButton(text="ѕкιρ ‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="▷ яєѕυмє", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="яєρℓαу ↺", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="мσяє", callback_data=f"PanelMarkup None|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def stream_markup2(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons


def stream_markup_timer2(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)

    if 0 < umm <= 40:
        bar = "◉——————————"
    elif 10 < umm < 20:
        bar = "—◉—————————"
    elif 20 < umm < 30:
        bar = "——◉————————"
    elif 30 <= umm < 40:
        bar = "———◉———————"
    elif 40 <= umm < 50:
        bar = "————◉——————"
    elif 50 <= umm < 60:
        bar = "——————◉————"
    elif 50 <= umm < 70:
        bar = "———————◉———"
    else:
        bar = "——————————◉"

    buttons = [
        [
            InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")
        ],
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(text=_["CLOSEMENU_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons


def panel_markup_1(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(text="ѕнυƒƒℓє", callback_data=f"ADMIN Shuffle|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="ℓσσρ ↺", callback_data=f"ADMIN Loop|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="◁ 10 ѕєc", callback_data=f"ADMIN 1|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="10 ѕєc ▷", callback_data=f"ADMIN 2|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="нσмє", callback_data=f"Pages Back|2|{videoid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="ηєχт", callback_data=f"Pages Forw|2|{videoid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(text="🕒 0.5x", callback_data=f"SpeedUP {chat_id}|0.5", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕓 0.75x", callback_data=f"SpeedUP {chat_id}|0.75", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕤 1.0x", callback_data=f"SpeedUP {chat_id}|1.0", style=enums.ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton(text="🕤 1.5x", callback_data=f"SpeedUP {chat_id}|1.5", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕛 2.0x", callback_data=f"SpeedUP {chat_id}|2.0", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="вαcк", callback_data=f"Pages Back|1|{videoid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def panel_markup_5(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=enums.ButtonStyle.SUCCESS,
            ),
        ],
        [
            InlineKeyboardButton(text="ραυѕє", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="sᴛᴏᴘ", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
            InlineKeyboardButton(text="sᴋɪᴘ", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="ʀᴇsᴜᴍᴇ", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="ʀᴇᴘʟᴀʏ", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="нσмє", callback_data=f"MainMarkup {videoid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="ηєχт", callback_data=f"Pages Forw|1|{videoid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="🕒 0.5x", callback_data=f"SpeedUP {chat_id}|0.5", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕓 0.75x", callback_data=f"SpeedUP {chat_id}|0.75", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕤 1.0x", callback_data=f"SpeedUP {chat_id}|1.0", style=enums.ButtonStyle.SUCCESS),
        ],
        [
            InlineKeyboardButton(text="🕤 1.5x", callback_data=f"SpeedUP {chat_id}|1.5", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="🕛 2.0x", callback_data=f"SpeedUP {chat_id}|2.0", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="вαcк", callback_data=f"Pages Back|2|{videoid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def panel_markup_4(_, vidid, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)

    if 0 < umm <= 40:
        bar = "◉——————————"
    elif 10 < umm < 20:
        bar = "—◉—————————"
    elif 20 < umm < 30:
        bar = "——◉————————"
    elif 30 <= umm < 40:
        bar = "———◉———————"
    elif 40 <= umm < 50:
        bar = "————◉——————"
    elif 50 <= umm < 60:
        bar = "——————◉————"
    elif 50 <= umm < 70:
        bar = "———————◉———"
    else:
        bar = "——————————◉"

    buttons = [
        [
            InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")
        ],
        [
            InlineKeyboardButton(text="II ραυѕє", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢ ѕтσρ", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
            InlineKeyboardButton(text="ѕкιρ ‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="▷ яєѕυмє", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="яєρℓαу ↺", callback_data=f"ADMIN Replay|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
        [
            InlineKeyboardButton(text="нσмє", callback_data=f"MainMarkup {vidid}|{chat_id}", style=enums.ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def panel_markup_clone(_, vidid, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}", style=enums.ButtonStyle.SUCCESS),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}", style=enums.ButtonStyle.PRIMARY),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}", style=enums.ButtonStyle.DANGER),
        ],
        [
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close", style=enums.ButtonStyle.DANGER),
        ],
    ]
    return buttons
