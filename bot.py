#!/usr/bin/env python3
"""OpenClaw Agent Hub — Telegram 统一调度入口

管理所有 OpenClaw agents:
  /tcm <问题>       — 倪李中医知识库查询
  /sandpump <关键词> — 非洲沙泵情报搜索
  /air             — 空压站巡检状态
  /agents          — 查看所有 agent 状态
  /help            — 帮助
"""

import os, sys, asyncio, json, logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

# 导入 agent 处理器
sys.path.insert(0, os.path.dirname(__file__))
from agents.tcm_handler import handle_tcm_query
from agents.sandpump_handler import handle_sandpump_query
from agents.aircompressor_handler import handle_aircompressor_status
from agents.commander_handler import handle_agents_status

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# ─── 命令处理 ──────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *OpenClaw Agent Hub*\n\n"
        "我是你的智能调度中心，管理以下 Agent：\n\n"
        "🏥 `/tcm 桂枝汤` — 倪李中医知识库\n"
        "🏗️ `/sandpump 加纳` — 非洲沙泵情报\n"
        "🔧 `/air` — 空压站巡检\n"
        "📋 `/agents` — Agent 状态面板\n\n"
        "直接发消息我也会自动识别意图。",
        parse_mode="Markdown"
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "*OpenClaw Agent Hub 帮助*\n\n"
        "*中医传承 Agent*\n"
        "`/tcm 方剂名或病证` — 查询倪李知识库\n"
        "例：`/tcm 破格救心汤` `/tcm 桂枝汤`\n\n"
        "*沙泵情报 Agent*\n"
        "`/sandpump 国家/关键词` — 搜索情报\n"
        "例：`/sandpump 加纳金矿` `/sandpump 买家`\n\n"
        "*空压巡检 Agent*\n"
        "`/air` — 查看空压站状态\n\n"
        "*综合命令*\n"
        "`/agents` — 所有 agent 运行状态\n"
        "`/help` — 本帮助",
        parse_mode="Markdown"
    )

async def tcm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args) if context.args else ''
    if not query:
        await update.message.reply_text("请提供查询内容，如：`/tcm 桂枝汤`", parse_mode="Markdown")
        return
    await update.message.chat.send_action("typing")
    result = await handle_tcm_query(query)
    await update.message.reply_text(result, parse_mode="Markdown")

async def sandpump_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args) if context.args else ''
    if not query:
        await update.message.reply_text("请提供搜索关键词，如：`/sandpump 加纳`", parse_mode="Markdown")
        return
    await update.message.chat.send_action("typing")
    result = await handle_sandpump_query(query)
    await update.message.reply_text(result, parse_mode="Markdown")

async def air_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    result = await handle_aircompressor_status()
    await update.message.reply_text(result, parse_mode="Markdown")

async def agents_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.chat.send_action("typing")
    result = await handle_agents_status()
    await update.message.reply_text(result, parse_mode="Markdown")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """自动识别消息意图并路由"""
    text = update.message.text.strip()

    # 中医关键词
    tcm_keywords = ['方', '汤', '丸', '散', '经方', '伤寒', '金匮', '倪海厦', '李可', '附子',
                    '桂枝', '麻黄', '四逆', '当归', '黄芪', '人参', '甘草', '柴胡', '黄芩',
                    '感冒', '咳嗽', '发烧', '头痛', '失眠', '胃', '肝', '肾', '心', '肺', '脾',
                    '针灸', '穴位', '本草', '神农', '内经', '扶阳', '中医', '中药']

    # 沙泵关键词
    sandpump_keywords = ['沙泵', '玉柴', '柴油机', '金矿', '加纳', '尼日利亚', '非洲', '买家',
                         '潍柴', '淘金', '抽沙', '报关', '海关', '出口', '报价']

    # 空压关键词
    air_keywords = ['空压', '气站', '压缩机', '巡检', '气压']

    lower = text.lower()

    if any(kw in text for kw in tcm_keywords):
        await update.message.chat.send_action("typing")
        result = await handle_tcm_query(text)
    elif any(kw in text for kw in sandpump_keywords):
        await update.message.chat.send_action("typing")
        result = await handle_sandpump_query(text)
    elif any(kw in text for kw in air_keywords):
        await update.message.chat.send_action("typing")
        result = await handle_aircompressor_status()
    else:
        # 默认用中医 agent
        await update.message.chat.send_action("typing")
        result = await handle_tcm_query(text)

    await update.message.reply_text(result, parse_mode="Markdown")

# ─── 主入口 ────────────────────────────────────────

def main():
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ 请在 .env 文件中设置 TELEGRAM_BOT_TOKEN")
        print("   1. 去 Telegram 找 @BotFather 创建 bot")
        print("   2. 拿到 token 后写入 .env 文件")
        sys.exit(1)

    app = Application.builder().token(token).build()

    # 注册命令
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("tcm", tcm_cmd))
    app.add_handler(CommandHandler("sandpump", sandpump_cmd))
    app.add_handler(CommandHandler("air", air_cmd))
    app.add_handler(CommandHandler("agents", agents_cmd))

    # 消息自动路由
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("🤖 OpenClaw Agent Hub 启动中...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
