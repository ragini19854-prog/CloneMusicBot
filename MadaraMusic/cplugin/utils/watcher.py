from pyrogram import filters, Client
from pyrogram.types import Message

from MadaraMusic import app
from MadaraMusic.core.call import Lucky
# ✅ FIX: db import kiya taaki queue clear kar sakein
from MadaraMusic.misc import db

welcome = 20
close = 30

@Client.on_message(filters.video_chat_started, group=welcome)
@Client.on_message(filters.video_chat_ended, group=close)
async def video_chat_events(_, message: Message):
    # Stream ko force stop karega
    await Lucky.stop_stream_force(message.chat.id)
    
    # ✅ FIX: Queue ko manually clear kar rahe hain taaki bot fresh start kare
    try:
        db[message.chat.id] = []
    except:
        pass