"""综合调度 Agent — 状态面板、agent 管理"""

import json, os
from datetime import datetime

async def handle_agents_status():
    """返回所有 agent 状态面板"""

    # 倪李中医
    tcm_idx_path = '/Users/diannao/.openclaw/workspace/agents/nili-tcm-heritage/knowledge/_index.json'
    tcm_status = "🔴 离线"
    tcm_ni = tcm_li = tcm_total = 0
    if os.path.exists(tcm_idx_path):
        with open(tcm_idx_path) as f:
            tcm_idx = json.load(f)
        tcm_ni = len([d for d in tcm_idx['documents'] if d['source'] == '倪海厦'])
        tcm_li = len([d for d in tcm_idx['documents'] if d['source'] == '李可'])
        tcm_total = tcm_idx['total_docs']
        tcm_status = f"🟢 {tcm_total}篇 / {tcm_idx['total_chars']:,}字"

    # 沙泵情报
    intel_dir = '/Users/diannao/Desktop/非洲沙泵'
    sandpump_status = "🟢 在线"
    intel_count = 0
    if os.path.exists(intel_dir):
        intel_count = len([f for f in os.listdir(intel_dir) if f.endswith('.md')])
    else:
        sandpump_status = "🟡 目录未初始化"

    # 空压巡检
    air_status = "🟡 待开发"

    # 最近情报
    latest_intel = "无"
    if intel_count > 0:
        latest = sorted([f for f in os.listdir(intel_dir) if f.endswith('.md')],
                        reverse=True)[:3]
        latest_intel = '\n'.join(f'  • {f}' for f in latest)

    return (
        f"📋 *OpenClaw Agent Hub · 状态面板*\n"
        f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n\n"
        f"🏥 *倪李中医传承*\n"
        f"  状态：{tcm_status}\n"
        f"  倪海厦：{tcm_ni} 篇\n"
        f"  李可：{tcm_li} 篇\n\n"
        f"🏗️ *非洲沙泵情报*\n"
        f"  状态：{sandpump_status}\n"
        f"  情报文件：{intel_count} 个\n"
        f"  最近情报：\n{latest_intel}\n\n"
        f"🔧 *空压站巡检*\n"
        f"  状态：{air_status}\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📱 4 个 agent 注册 | 2 个就绪 | 1 个开发中 | 1 个待激活"
    )
