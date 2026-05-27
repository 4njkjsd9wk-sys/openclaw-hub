#!/usr/bin/env python3
import os, asyncio
TOKEN = os.environ["TG_TOKEN"]
from telegram import Update
from telegram.ext import Application, CommandHandler

async def start(u: Update, c):
    await u.message.reply_text("OpenClaw Agent Hub\n\n/tcm - TCM knowledge\n/sandpump - Pump intel\n/agents - Status")

async def tcm(u: Update, c):
    q = " ".join(c.args) if c.args else ""
    await u.message.reply_text(f"TCM Query: {q}\n\nNi Haixia 503 + Li Ke 49\nTotal 554 docs, 31.1M chars")

async def sandpump(u: Update, c):
    q = " ".join(c.args) if c.args else ""
    await u.message.reply_text(f"Sand Pump: {q}\n\nYuchai 260 diesel + pump\nGhana Mali Nigeria gold mining")

async def agents_cmd(u: Update, c):
    await u.message.reply_text("OpenClaw Agent Hub\nTCM: ONLINE\nSand Pump: ONLINE\nAir Compressor: DEV")

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tcm", tcm))
    app.add_handler(CommandHandler("sandpump", sandpump))
    app.add_handler(CommandHandler("agents", agents_cmd))
    await app.initialize()
    await app.start()
    await app.updater.start_polling(poll_interval=1.0, timeout=30)
    print("Bot running...")
    await asyncio.sleep(120)
    await app.updater.stop()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
