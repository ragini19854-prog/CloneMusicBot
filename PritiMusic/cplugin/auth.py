from pyrogram import filters, Client
from pyrogram.types import Message
from PritiMusic import app
from PritiMusic.utils import extract_user, int_to_alpha
from PritiMusic.utils.database import (
    delete_authuser,
    get_authuser,
    get_authuser_names,
    save_authuser,
)
from PritiMusic.utils.decorators import AdminActual, language
from PritiMusic.utils.inline import close_markup
from config import BANNED_USERS, adminlist

@Client.on_message(filters.command("auth") & filters.group & ~BANNED_USERS)
@AdminActual
async def auth(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    token = int_to_alpha(user.id)
    
    _check = await get_authuser_names(message.chat.id)
    count = len(_check)
    
    if int(count) == 25:
        return await message.reply_text(_["auth_1"])
        
    if token not in _check:
        assis = {
            "auth_user_id": user.id,
            "auth_name": user.first_name,
            "admin_id": message.from_user.id,
            "admin_name": message.from_user.first_name,
        }
        
        if message.chat.id not in adminlist:
            adminlist[message.chat.id] = []
            
        if user.id not in adminlist[message.chat.id]:
            adminlist[message.chat.id].append(user.id)
        
        await save_authuser(message.chat.id, token, assis)
        return await message.reply_text(_["auth_2"].format(user.mention))
    else:
        return await message.reply_text(_["auth_3"].format(user.mention))

@Client.on_message(filters.command("unauth") & filters.group & ~BANNED_USERS)
@AdminActual
async def unauthusers(client, message: Message, _):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text(_["general_1"])
    
    user = await extract_user(message)
    token = int_to_alpha(user.id)
    
    deleted = await delete_authuser(message.chat.id, token)
    
    if message.chat.id in adminlist:
        if user.id in adminlist[message.chat.id]:
            adminlist[message.chat.id].remove(user.id)
            
    if deleted:
        return await message.reply_text(_["auth_4"].format(user.mention))
    else:
        return await message.reply_text(_["auth_5"].format(user.mention))

@Client.on_message(filters.command(["authlist", "authusers"]) & filters.group & ~BANNED_USERS)
@language
async def authusers(client, message: Message, _):
    auth_names = await get_authuser_names(message.chat.id)
    
    if not auth_names:
        return await message.reply_text(_["setting_4"])
    
    mystic = await message.reply_text(_["auth_6"])
    text = _["auth_7"].format(message.chat.title)
    
    j = 0
    for auth_token in auth_names:
        _auth_data = await get_authuser(message.chat.id, auth_token)
        
        if not _auth_data:
            continue
            
        user_id = _auth_data["auth_user_id"]
        admin_id = _auth_data["admin_id"]
        admin_name = _auth_data["admin_name"]
        
        try:
            user_obj = await client.get_users(user_id)
            user_name = user_obj.first_name
            j += 1
        except Exception:
            continue
            
        text += f"{j}➤ {user_name} [<code>{user_id}</code>]\n"
        text += f"   {_['auth_8']} {admin_name} [<code>{admin_id}</code>]\n\n"
        
    await mystic.edit_text(text, reply_markup=close_markup(_))
