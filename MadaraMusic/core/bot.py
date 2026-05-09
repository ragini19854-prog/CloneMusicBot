from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER

FOOTER = "\n\n<b>•──────────────────────•\n🌺 ᴘᴏᴡєʀєᴅ ʙʏ » |𝐌 ᴀ ᴅ ᴀ ʀ ᴀ •| <a href='http://t.me/YOUR_MADARA_BRO'>⚡</a>\n•──────────────────────•</b>"


def _append_footer(text: str) -> str:
    if not text:
        return text
    if "YOUR_MADARA_BRO" in text:
        return text
    return text + FOOTER


class Madara(Client):
    def __init__(self):
        LOGGER(__name__).info(f"Starting Bot...")
        super().__init__(
            name="MadaraMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await super().send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ sᴛᴀʀᴛᴇᴅ :</b><u>\n\nɪᴅ : <code>{self.id}</code>\nɴᴀᴍᴇ : {self.name}\nᴜsᴇʀɴᴀᴍᴇ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot has failed to access the log group/channel. Make sure that you have added your bot to your log group/channel."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot has failed to access the log group/channel.\n  Reason : {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Please Promote your bot as an admin in your log group/channel."
            )
            exit()
        LOGGER(__name__).info(f"Music Bot Started as {self.name}")

    async def stop(self):
        await super().stop()

    async def send_message(self, *args, **kwargs):
        if "text" in kwargs and kwargs["text"]:
            kwargs["text"] = _append_footer(kwargs["text"])
        elif len(args) >= 2 and isinstance(args[1], str):
            args = list(args)
            args[1] = _append_footer(args[1])
            args = tuple(args)
        return await super().send_message(*args, **kwargs)

    async def send_photo(self, *args, **kwargs):
        if "caption" in kwargs and kwargs["caption"]:
            kwargs["caption"] = _append_footer(kwargs["caption"])
        return await super().send_photo(*args, **kwargs)

    async def edit_message_text(self, *args, **kwargs):
        if "text" in kwargs and kwargs["text"]:
            kwargs["text"] = _append_footer(kwargs["text"])
        elif len(args) >= 3 and isinstance(args[2], str):
            args = list(args)
            args[2] = _append_footer(args[2])
            args = tuple(args)
        return await super().edit_message_text(*args, **kwargs)

    async def send_video(self, *args, **kwargs):
        if "caption" in kwargs and kwargs["caption"]:
            kwargs["caption"] = _append_footer(kwargs["caption"])
        return await super().send_video(*args, **kwargs)

    async def send_audio(self, *args, **kwargs):
        if "caption" in kwargs and kwargs["caption"]:
            kwargs["caption"] = _append_footer(kwargs["caption"])
        return await super().send_audio(*args, **kwargs)

    async def send_document(self, *args, **kwargs):
        if "caption" in kwargs and kwargs["caption"]:
            kwargs["caption"] = _append_footer(kwargs["caption"])
        return await super().send_document(*args, **kwargs)
