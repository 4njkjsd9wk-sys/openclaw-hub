#!/usr/bin/env python3
"""OpenClaw Agent Hub Bot - GitHub Actions Runner"""
import os, asyncio

TOKEN = os.environ["TG_TOKEN"]

from telegram import Update
from telegram.ext import Application, CommandHandler

async def start(u: Update, c):
    await u.message.reply_text(
        "🤖 *OpenClaw Agent Hub*

"
        "📚 /tcm 倪李中医知识库 (554篇/3110万字)
"
        "🏗️ /sandpump 非洲沙泵情报
"
        "📋 /agents 状态面板
"
        "📱 Telegram 管理所有 Agent",
        parse_mode="Markdown"
    )

async def tcm(u: Update, c):
    q = " ".join(c.args) if c.args else "桂枝汤"
    await u.message.reply_text(
        f"📚 *倪李中医传承 · 查询: {q}*

"
        f"知识库就绪:
"
        f"• 倪海厦 503篇 — 伤寒金匮本草针灸理论体系
"
        f"• 李可 49篇 — 急危重症经方实战经验
"
        f"• 总计 554篇 / 3110万字

"
        f"完整查询请使用飞书/Dify平台连接本地知识库",
        parse_mode="Markdown"
    )

async def sandpump(u: Update, c):
    q = " ".join(c.args) if c.args else "非洲"
    await u.message.reply_text(
        f"🏗️ *非洲沙泵情报 · {q}*

"
        f"情报系统: 🟢 在线
"
        f"目标市场: 加纳/马里/尼日利亚/布基纳法索
"
        f"产品: 玉柴260柴油机 + 沙泵组合
"
        f"核心场景: 金矿抽沙洗金

"
        f"情报目录: ~/Desktop/非洲沙泵/",
        parse_mode="Markdown"
    )

async def agents_cmd(u: Update, c):
    await u.message.reply_text(
        "📋 *OpenClaw Agent Hub*

"
        "🏥 倪李中医: 🟢 554篇/3110万字
"
        "🏗️ 非洲沙泵: 🟢 情报就绪
"
        "🔧 空压巡检: 🟡 待开发
"
        "🤖 Telegram Bot: 🟢 运行中

"
        "GitHub: 4njkjsd9wk-sys/openclaw-hub",
        parse_mode="Markdown"
    )

async def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("tcm", tcm))
    app.add_handler(CommandHandler("sandpump", sandpump))
    app.add_handler(CommandHandler("agents", agents_cmd))
    
    await app.initialize()
    await app.start()
    await app.updater.start_polling(poll_interval=1.0, timeout=30)
    print("Bot polling...")
    await asyncio.sleep(120)
    await app.updater.stop()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())
