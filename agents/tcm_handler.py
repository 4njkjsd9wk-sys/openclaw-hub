"""倪李中医知识库 Agent — Telegram 适配器"""

import json, os, re

KB_INDEX = '/Users/diannao/.openclaw/workspace/agents/nili-tcm-heritage/knowledge/_index.json'

def _load_index():
    with open(KB_INDEX) as f:
        return json.load(f)

def _search_knowledge_base(query, top_k=5):
    """在知识库中搜索相关内容"""
    idx = _load_index()
    results = []

    for doc in idx['documents']:
        name = doc.get('name', '')
        score = 0
        for char in query:
            if char in name:
                score += 1

        if score > 0:
            results.append((score, doc))

    results.sort(key=lambda x: x[0], reverse=True)

    # 取 top_k 个最相关的
    top_docs = results[:top_k]
    return top_docs

def _read_doc_excerpt(path, query, max_chars=800):
    """读取文档中与查询相关的片段"""
    if not os.path.exists(path):
        return None
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()

        # 跳过文件头
        text = re.sub(r'^#.*?(?=\n\n)', '', text, flags=re.DOTALL)

        # 找包含关键词的段落
        paragraphs = text.split('\n\n')
        relevant = []
        for p in paragraphs:
            if any(kw in p for kw in query):
                relevant.append(p.strip())

        if relevant:
            excerpt = '\n\n'.join(relevant[:3])
            if len(excerpt) > max_chars:
                excerpt = excerpt[:max_chars] + '...'
            return excerpt
        else:
            # 返回开头部分
            clean = text.strip()[:max_chars]
            return clean + '...' if len(text) > max_chars else clean
    except:
        return None

async def handle_tcm_query(query):
    """处理中医查询，遵循 SOUL.md 铁律"""
    idx = _load_index()

    # 检查知识库是否涉及
    docs = _search_knowledge_base(query)

    ni_count = len([d for d in idx['documents'] if d['source'] == '倪海厦'])
    li_count = len([d for d in idx['documents'] if d['source'] == '李可'])

    if not docs or docs[0][0] < 2:
        return (
            f"📚 *倪李中医知识库*\n\n"
            f"根据您提供的中医知识体系，未找到与「{query}」直接相关的信息。\n\n"
            f"请补充该部分知识，或确认是否允许我基于已有知识进行合理推断。\n\n"
            f"📊 当前知识库：倪海厦 {ni_count} 篇 | 李可 {li_count} 篇 | 总计 {idx['total_docs']} 篇\n"
            f"📝 {idx['total_chars']:,} 字"
        )

    # 组装回答
    lines = [f"📚 *倪李中医知识库 · 查询结果*\n"]
    lines.append(f"🔍 查询：{query}\n")

    shown = 0
    for score, doc in docs[:8]:
        name = doc['name'].replace('_', ' ').replace('.txt', '').replace('.pdf', '')
        source = doc['source']
        chars = doc['chars']
        category = doc.get('category', '')

        # 读取原文片段
        path = doc.get('path', '')
        excerpt = _read_doc_excerpt(path, query, 600) if path else None

        if excerpt and len(excerpt) > 50:
            lines.append(f"*{source}* · {category}")
            lines.append(f"📄 {name[:60]}")
            lines.append(f"```\n{excerpt[:500]}\n```")
            lines.append(f"📊 {chars:,}字\n")
            shown += 1
            if shown >= 5:
                break

    if shown == 0:
        lines.append(f"找到 {len(docs)} 篇相关文档，但未提取到有效内容。请直接查阅原文。")

    lines.append(f"---\n📊 倪海厦 {ni_count} 篇 | 李可 {li_count} 篇 | 总计 {idx['total_docs']} 篇")

    return '\n'.join(lines)
