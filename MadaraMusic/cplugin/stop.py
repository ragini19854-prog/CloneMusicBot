from pyrogram import filters, Client
from pyrogram.types import Message

from MadaraMusic import app
from MadaraMusic.core.call import Madara
from MadaraMusic.utils.database import set_loop
from MadaraMusic.utils.inline import close_markup
from config import BANNED_USERS
from MadaraMusic.misc import db

# ✅ IMPORT NEW ADMIN CHECKER (For Clone Support)
from MadaraMusic.cplugin.utils.decorators.admins import AdminRightsCheck

@Client.on_message(
    filters.command(
        ["end", "stop", "cend", "cstop"],
        prefixes=["/", "!", "%", ",", "", ".", "@", "#"],
    )
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck # <-- Ab ye Clone Owner/Sudo ko allow karega
async def stop_music(cli, message: Message, _, chat_id):
    if not len(message.command) == 1:
        return
    
    # Stream Stop Karega
    await Madara.stop_stream(chat_id)
    
    # Loop Reset Karega
    await set_loop(chat_id, 0)
    
    # Queue Empty (Safety Fix)
    try:
        db[chat_id] = []
    except:
        pass
        
    await message.reply_text(
        _["admin_5"].format(message.from_user.mention), reply_markup=close_markup(_)
    )