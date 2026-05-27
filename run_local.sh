#!/bin/bash
cd /Users/diannao/.openclaw/workspace/telegram-hub
while true; do
    python3 -c "
import asyncio, os, sys
sys.path.insert(0, 'agents')
from telegram import Bot
from telegram.ext import Application, CommandHandler
from agents.tcm_handler import handle_tcm_query
from agents.sandpump_handler import handle_sandpump_query
from agents.commander_handler import handle_agents_status

TOKEN = open('.env').read().split('=')[1].strip()

async def start(u,c): await u.message.reply_text('OpenClaw Agent Hub')
async def tcm(u,c):
    q=' '.join(c.args) if c.args else '桂枝汤'
    r=await handle_tcm_query(q)
    await u.message.reply_text(r[:4000])
async def sandpump(u,c):
    q=' '.join(c.args) if c.args else '非洲'  
    r=await handle_sandpump_query(q)
    await u.message.reply_text(r[:4000])
async def agents(u,c):
    r=await handle_agents_status()
    await u.message.reply_text(r[:4000])

app = Application.builder().token(TOKEN).build()
for h in [CommandHandler('start',start),CommandHandler('tcm',tcm),
          CommandHandler('sandpump',sandpump),CommandHandler('agents',agents)]:
    app.add_handler(h)

async def run():
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    print('Bot running...')
    await asyncio.Event().wait()

try:
    asyncio.run(run())
except KeyboardInterrupt:
    pass
"
    echo "Bot 断开，60秒后重试..."
    sleep 60
done
