# ✅ FIX: db import kiya (baaki files ke sath sync karne ke liye)
from MadaraMusic.misc import db


async def put(
    chat_id,
    title,
    duration,
    videoid,
    file_path,
    ruser,
    user_id,
    streamtype="audio",  # Default audio rakha hai, video ke liye change hoga
):
    put_f = {
        "title": title,
        "dur": duration,       # skip.py mein ["dur"] use hota hai
        "file": file_path,     # skip.py mein ["file"] use hota hai
        "vidid": videoid,      # skip.py mein ["vidid"] use hota hai
        "by": ruser,           # skip.py mein ["by"] use hota hai
        "user_id": user_id,
        "streamtype": streamtype, # Important for video/audio check
        "played": 0,           # Seek bar ke liye zaroori hai
        "seconds": 0,          # Duration calculation ke liye
    }
    
    get = db.get(chat_id)
    if get:
        db[chat_id].append(put_f)
    else:
        db[chat_id] = []
        db[chat_id].append(put_f)