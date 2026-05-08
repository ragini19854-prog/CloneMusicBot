# PritiMusic - Telegram Music Bot

## Overview
A Telegram Music Bot that streams high-quality music in Telegram voice chats. Built with Python using pyrofork, py-tgcalls, and motor (MongoDB).

## Required Environment Variables
Before the bot can run, you must set these secrets in the Replit Secrets tab:

- `BOT_TOKEN` — Your Telegram bot token (from @BotFather)
- `API_ID` — Telegram API ID (from my.telegram.org)
- `API_HASH` — Telegram API Hash (from my.telegram.org)
- `STRING_SESSION` — Pyrogram string session for the userbot assistant
- `MONGO_DB_URI` — MongoDB connection URI
- `LOGGER_ID` — Telegram chat/channel ID for bot logs
- `OWNER_ID` — Your Telegram user ID

## Running the Bot
The bot is configured to run via the "Start application" workflow using:
```
python3 -m PritiMusic
```

## Key Changes Made During Import
1. Fixed `config.py` — corrected broken `getenv()` calls that had actual values as keys instead of env var names
2. Fixed `PritiMusic/core/call.py` — updated from pytgcalls v0.x API to v2.x API:
   - `AudioPiped`/`AudioVideoPiped` → `MediaStream`
   - `join_group_call` → `play`
   - `leave_group_call` → `leave_call`
   - `pause_stream`/`resume_stream` → `pause`/`resume`
   - Old decorators (`on_kicked`, `on_stream_end`, etc.) → `on_update` with `ChatUpdate`/`StreamEnded`
3. Added `force_stop_stream` method alias
4. Fixed `requirements.txt` — removed invalid `py-tgcalls==0.9.7` pin (now uses latest)
5. Removed hardcoded pillow version pin that caused build failure on Python 3.12

## User Preferences
- Keep code compatible with pytgcalls v2.x API
