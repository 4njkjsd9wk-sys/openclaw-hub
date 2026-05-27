"""非洲沙泵情报 Agent — Telegram 适配器"""

import os, json
from datetime import datetime

INTEL_DIR = '/Users/diannao/Desktop/非洲沙泵'

def _list_latest_intel(n=5):
    """列出最新情报文件"""
    if not os.path.exists(INTEL_DIR):
        return []
    files = []
    for f in os.listdir(INTEL_DIR):
        if f.endswith('.md') and not f.startswith('_'):
            path = os.path.join(INTEL_DIR, f)
            mtime = os.path.getmtime(path)
            files.append((f, mtime, path))

    files.sort(key=lambda x: x[1], reverse=True)
    return files[:n]

async def handle_sandpump_query(query):
    """处理沙泵情报查询"""

    # 检查是否有情报文件夹
    if not os.path.exists(INTEL_DIR):
        return (
            f"🏗️ *非洲沙泵情报 Agent*\n\n"
            f"情报目录尚未初始化。请先在桌面创建「非洲沙泵」文件夹。\n\n"
            f"当前查询：{query}"
        )

    latest = _list_latest_intel(10)

    # 搜索相关情报
    relevant_files = []
    for fname, mtime, path in latest:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            if any(kw.lower() in content.lower() for kw in query.split()):
                relevant_files.append((fname, mtime, content[:800]))
        except:
            pass

    lines = [f"🏗️ *非洲沙泵情报 Agent*\n"]
    lines.append(f"🔍 查询：{query}\n")

    if relevant_files:
        lines.append(f"📋 找到 {len(relevant_files)} 条相关情报：\n")
        for fname, mtime, excerpt in relevant_files[:3]:
            dt = datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
            lines.append(f"📄 *{fname}* ({dt})")
            lines.append(f"```\n{excerpt[:500]}\n```\n")
    else:
        lines.append(f"⚠️ 未找到与「{query}」直接相关的情报。\n")

    # 列出最新文件
    lines.append(f"---\n📂 *最新情报文件* ({len(os.listdir(INTEL_DIR))} 个)：")
    for fname, mtime, _ in latest[:6]:
        dt = datetime.fromtimestamp(mtime).strftime('%m-%d %H:%M')
        lines.append(f"  • {fname} ({dt})")

    return '\n'.join(lines)
