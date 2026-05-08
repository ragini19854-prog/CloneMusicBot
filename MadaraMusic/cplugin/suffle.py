import random

from pyrogram import filters, Client
from pyrogram.types import Message

from MadaraMusic import app
from MadaraMusic.misc import db
from MadaraMusic.utils.inline import close_markup
from config import BANNED_USERS

# ✅ IMPORT NEW ADMIN CHECKER (For Clone Support)
from MadaraMusic.cplugin.utils.decorators.admins import AdminRightsCheck

@Client.on_message(
    filters.command(["shuffle", "cshuffle"]) & filters.group & ~BANNED_USERS
)
@AdminRightsCheck # <-- Ab ye Clone Owner/Sudo ko allow karega
async def shuffle_music(client, message: Message, _, chat_id):
    check = db.get(chat_id)
    if not check:
        return await message.reply_text(_["queue_2"])
    
    try:
        # Jo gaana chal raha hai usse nikaal lo (pop)
        popped = check.pop(0)
    except:
        return await message.reply_text(_["admin_15"], reply_markup=close_markup(_))
    
    check = db.get(chat_id)
    if not check:
        # Agar queue mein aur gaane nahi hain to wapis daal do
        check.insert(0, popped)
        return await message.reply_text(_["admin_15"], reply_markup=close_markup(_))
    
    # Baaki queue ko shuffle karo
    random.shuffle(check)
    
    # Jo gaana chal raha tha use wapis sabse upar laga do
    check.insert(0, popped)
    
    await message.reply_text(
        _["admin_16"].format(message.from_user.mention), reply_markup=close_markup(_)
    )