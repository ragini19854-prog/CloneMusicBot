import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.raw import functions, types
from MadaraMusic import app
from MadaraMusic.misc import SUDOERS  # ✅ Correct Import
from MadaraMusic.utils.database import clonebotdb
from config import API_ID, API_HASH

REASONS = {
    "spam": types.InputReportReasonSpam(),
    "fake": types.InputReportReasonFake(),
    "violence": types.InputReportReasonViolence(),
    "porn": types.InputReportReasonPornography(),
    "child": types.InputReportReasonChildAbuse(),
    "other": types.InputReportReasonOther(),
}

# ✅ FIX: Removed filters.user() wrapper
@app.on_message(filters.command(["greport", "massreport"]) & SUDOERS)
async def global_report(client: Client, message: Message):
    if len(message.command) < 2:
        return await message.reply_text(
            "ℹ️ **Mass Report Tool** (Owner Only)\n\n"
            "**Usage:** `/greport [Target] [Reason]`\n"
            "**Reasons:** spam, fake, violence, porn, child\n"
            "**Example:** `/greport @BadUser spam`"
        )

    target = message.command[1]
    reason_txt = message.command[2].lower() if len(message.command) > 2 else "spam"
    reason = REASONS.get(reason_txt, types.InputReportReasonSpam())

    msg = await message.reply_text("🔄 **Loading Clones...**")

    # Fetch Sessions
    sessions = []
    async for bot in clonebotdb.find({"session_string": {"$exists": True}}):
        if bot.get("session_string"):
            sessions.append(bot["session_string"])

    if not sessions:
        return await msg.edit_text("❌ **No Clones Connected!**")

    await msg.edit_text(f"🚀 **Attacking {target} with {len(sessions)} Clones...**")

    async def report_worker(session, wid):
        try:
            cli = Client(f"r_{wid}", api_id=API_ID, api_hash=API_HASH, session_string=session, no_updates=True, in_memory=True)
            await cli.start()
            try:
                peer = await cli.resolve_peer(target)
                await cli.invoke(
                    functions.account.ReportPeer(
                        peer=peer,
                        reason=reason,
                        message=f"Mass Report: {reason_txt}"
                    )
                )
                await cli.stop()
                return True
            except Exception:
                await cli.stop()
                return False
        except:
            return False

    tasks = [report_worker(sessions[i], i) for i in range(len(sessions))]
    results = await asyncio.gather(*tasks)
    
    success = results.count(True)
    await message.reply_text(
        f"🏁 **Report Completed!**\n\n"
        f"🎯 **Target:** `{target}`\n"
        f"✅ **Successful Reports:** {success}\n"
        f"❌ **Failed:** {len(sessions) - success}"
    )