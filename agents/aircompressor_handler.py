"""空压站巡检 Agent — Telegram 适配器"""

async def handle_aircompressor_status():
    """返回空压站状态"""
    return (
        f"🔧 *广西空压站巡检 Agent*\n\n"
        f"状态：🟢 在线\n"
        f"当前任务：等待巡检指令\n\n"
        f"可用命令：\n"
        f"  • `/air` — 查看状态\n"
        f"  • 发送空压站数据 — 自动分析\n\n"
        f"📊 本 agent 尚在开发中，完整功能即将上线。"
    )
