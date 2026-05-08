from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# --- OPTION 1: Static (Jo aapne bheja) ---
# Note: Ye tabhi use karein agar aapke paas 'resume_cb' ka alag handler ho.
buttons = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(text="▷", callback_data="resume_cb"),
            InlineKeyboardButton(text="II", callback_data="pause_cb"),
            InlineKeyboardButton(text="‣‣I", callback_data="skip_cb"),
            InlineKeyboardButton(text="▢", callback_data="end_cb"),
        ]
    ]
)

close_key = InlineKeyboardMarkup(
    [[InlineKeyboardButton(text="✯ ᴄʟᴏsᴇ ✯", callback_data="close")]]
)


# --- OPTION 2: Dynamic (RECOMMENDED) ---
# Ye function use karein taaki 'resume.py' aur 'pause.py' ke logic ke sath match kare.
# Isme hum 'chat_id' pass karte hain taaki bot confuse na ho.

def stream_markup(chat_id):
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
                InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
                InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
                InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
            ],
            [
                InlineKeyboardButton(text="✯ ᴄʟᴏsᴇ ✯", callback_data="close")
            ]
        ]
    )