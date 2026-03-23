#!/usr/bin/env python3
"""
GitHub 热门项目日报获取器
从 GitHub 获取热门开源项目并生成中文日报
"""

import os
import sys
import json
import argparse
import time
from datetime import datetime, timedelta
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from typing import List, Dict, Any


# 翻译映射表
TRANSLATIONS = {
    # 常见项目描述翻译
    "freeCodeCamp.org's open-source codebase and curriculum. Learn math, programming, and computer science for free.": "freeCodeCamp.org 的开源代码库和课程。免费学习数学、编程和计算机科学。",
    "A collective list of free APIs": "免费 API 合集",
    "Freely available programming books": "免费编程书籍",
    "Interactive roadmaps, guides and other educational content to help developers grow in their careers.": "帮助开发者职业成长的交互式路线图、指南和其他教育内容。",
    "Learn how to design large-scale systems. Prep for the system design interview. Includes Anki flashcards.": "学习如何设计大规模系统。为系统设计面试做准备。包含 Anki 记忆卡片。",
    "Run OpenClaw securely inside NVIDIA OpenShell with managed inference": "在 NVIDIA OpenShell 中安全运行 OpenClaw，提供托管推理服务",
    "Fully autonomous & self-evolving research from idea to paper. Chat an Idea. Get a Paper.": "从想法到论文的全自主、自进化研究。聊一个想法，获得一篇论文。",
    "ClawTeam: Agent Swarm Intelligence (One Command → Full Automation)": "ClawTeam：智能体群体智能（一条命令 → 全自动）",
    "A collection of 130+ specialized Codex subagents covering a wide range of development use cases.": "130+ 个专业 Codex 子代理的集合，涵盖广泛的开发用例。",
    "Your personal intelligence agent. Watches the world from multiple data sources and pings you when important things happen.": "你的个人智能代理。从多个数据源监控世界，重要事件发生时通知你。",
    "Make Any Website & Tool Your CLI. A universal CLI Hub and AI-native runtime. Transform any website into a CLI command.": "让任何网站和工具成为你的 CLI。通用 CLI 中心和 AI 原生运行时。将任何网站转换为 CLI 命令。",
    "ARIS (Auto-Research-In-Sleep) — Lightweight Markdown-only skills for autonomous ML research": "ARIS（睡眠中自动研究）—— 用于自主 ML 研究的轻量级纯 Markdown 技能",
    "Give your AI agent access to your live Chrome session — works out of the box, connects to tabs you already have open": "让你的 AI 代理访问你正在运行的 Chrome 会话 —— 开箱即用，连接你已打开的标签页",
    "No description": "暂无描述",
    "Unknown": "未知",
}


def get_github_token() -> str:
    """从环境变量获取 GitHub Token"""
    return os.environ.get('GITHUB_TOKEN', '')


def translate_text(text: str) -> str:
    """翻译文本为中文"""
    if not text:
        return "暂无描述"
    
    # 直接匹配完整描述
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    
    # 部分匹配常见开头
    if text.startswith("A collective list of"):
        return "免费 API 资源合集"
    if text.startswith("Interactive roadmaps"):
        return "帮助开发者成长的交互式路线图和教育内容"
    if text.startswith("Learn how to design"):
        return "学习大规模系统设计，准备系统设计面试"
    if "open-source codebase" in text.lower():
        return "开源代码库和课程平台"
    if "autonomous" in text.lower() and "research" in text.lower():
        return "自主研究代理，从想法到论文"
    if "intelligence agent" in text.lower():
        return "个人智能代理，多数据源监控"
    if "CLI" in text.upper() and "website" in text.lower():
        return "将网站转换为 CLI 命令的工具"
    
    return text


def translate_language(lang: str) -> str:
    """翻译编程语言名称为中文"""
    lang_map = {
        "Python": "Python",
        "JavaScript": "JavaScript",
        "TypeScript": "TypeScript",
        "Java": "Java",
        "Go": "Go",
        "Rust": "Rust",
        "C++": "C++",
        "C": "C",
        "C#": "C#",
        "Ruby": "Ruby",
        "PHP": "PHP",
        "Swift": "Swift",
        "Kotlin": "Kotlin",
        "Unknown": "未知",
        None: "未知",
    }
    return lang_map.get(lang, lang or "未知")


def make_request(url: str, headers: Dict[str, str] = None) -> Dict[str, Any]:
    """发送 HTTP 请求并返回 JSON 响应"""
    req_headers = {
        'User-Agent': 'GitHub-Trending-Digest/1.0',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    token = get_github_token()
    if token:
        req_headers['Authorization'] = f'token {token}'
    
    if headers:
        req_headers.update(headers)
    
    try:
        req = Request(url, headers=req_headers)
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode('utf-8'))
    except HTTPError as e:
        if e.code == 403:
            print("警告：API 速率限制已达上限。建议设置 GITHUB_TOKEN 以获得更高的限制。", file=sys.stderr)
        elif e.code == 422:
            print(f"警告：查询参数无效", file=sys.stderr)
        else:
            print(f"HTTP 错误 {e.code}: {e.reason}", file=sys.stderr)
        return {}
    except Exception as e:
        print(f"获取数据时出错: {e}", file=sys.stderr)
        return {}


def fetch_trending_repos(since: str = "daily", language: str = None) -> List[Dict[str, Any]]:
    """获取 GitHub 热门仓库"""
    from urllib.parse import quote
    
    # 根据时间范围计算日期
    days = 1 if since == "daily" else 7 if since == "weekly" else 30
    date = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
    
    query = f"created:>{date}"
    if language:
        query += f" language:{language}"
    
    encoded_query = quote(query, safe='/:>=<')
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=15"
    
    data = make_request(url)
    return data.get('items', [])


def fetch_ai_ml_projects() -> List[Dict[str, Any]]:
    """获取 AI/ML 相关的热门项目"""
    from urllib.parse import quote
    
    # 计算最近项目的日期
    date = (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d')
    
    # 使用多个查询搜索 AI/ML 相关仓库
    ai_queries = [
        "AI created:>" + date,
        "machine learning created:>" + date,
        "deep learning created:>" + date,
        "LLM created:>" + date,
        "GPT created:>" + date,
    ]
    
    all_repos = {}
    
    for query in ai_queries:
        encoded_query = quote(query, safe='/:>=<')
        url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=5"
        
        data = make_request(url)
        items = data.get('items', [])
        
        for item in items:
            repo_id = item.get('id')
            if repo_id and repo_id not in all_repos:
                all_repos[repo_id] = item
        
        # 小延迟以避免触发速率限制
        time.sleep(0.5)
    
    # 按 star 数排序并返回前 10
    sorted_repos = sorted(all_repos.values(), key=lambda x: x.get('stargazers_count', 0), reverse=True)
    return sorted_repos[:10]


def fetch_most_starred() -> List[Dict[str, Any]]:
    """获取最近创建的最多 star 的仓库"""
    return fetch_trending_repos(since="weekly")


def fetch_fastest_growing() -> List[Dict[str, Any]]:
    """获取增长最快的仓库（最近有活跃推送）"""
    from urllib.parse import quote
    
    # 获取最近有推送的高 star 仓库
    date = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
    query = f"pushed:>{date}"
    
    encoded_query = quote(query, safe='/:>=<')
    url = f"https://api.github.com/search/repositories?q={encoded_query}&sort=stars&order=desc&per_page=15"
    
    data = make_request(url)
    return data.get('items', [])


def format_repo(repo: Dict[str, Any]) -> str:
    """格式化单个仓库信息"""
    name = repo.get('full_name', '未知')
    description = translate_text(repo.get('description', ''))
    language = translate_language(repo.get('language'))
    stars = repo.get('stargazers_count', 0)
    url = repo.get('html_url', '')
    
    # 如果描述太长则截断
    if len(description) > 100:
        description = description[:97] + '...'
    
    return f"""
📦 **{name}**
   {description}
   ⭐ {stars:,} 星标 | 🔤 {language}
   🔗 {url}
"""


def format_digest(hottest: List[Dict], trending: List[Dict], ai_ml: List[Dict]) -> str:
    """格式化完整的日报"""
    today = datetime.now().strftime('%Y年%m月%d日')
    
    sections = [
        f"# 🔥 GitHub 热门项目日报 - {today}",
        "",
        "## 📈 最热门项目",
        "最近创建的获得最多星标的项目：",
    ]
    
    if hottest:
        for repo in hottest[:5]:
            sections.append(format_repo(repo))
    else:
        sections.append("_暂无数据 - 可能已达到 API 速率限制_")
    
    sections.extend([
        "",
        "## 🚀 增长最快",
        "近期活跃度最高的项目：",
    ])
    
    if trending:
        for repo in trending[:5]:
            sections.append(format_repo(repo))
    else:
        sections.append("_暂无数据 - 可能已达到 API 速率限制_")
    
    sections.extend([
        "",
        "## 🤖 人工智能/机器学习",
        "AI/ML 领域的新热门项目：",
    ])
    
    if ai_ml:
        for repo in ai_ml[:5]:
            sections.append(format_repo(repo))
    else:
        sections.append("_暂无数据 - 可能已达到 API 速率限制_")
    
    sections.extend([
        "",
        "---",
        "💡 *提示：设置 GITHUB_TOKEN 环境变量可获得更高的 API 调用限额*",
    ])
    
    return '\n'.join(sections)


def send_notification(digest: str, channel: str = None):
    """通过 OpenClaw 消息系统发送日报"""
    import subprocess
    import shutil
    
    channel = channel or os.environ.get('NOTIFY_CHANNEL', '')
    
    if not channel:
        print("警告：未配置通知频道。请设置 NOTIFY_CHANNEL 环境变量。")
        print("\n" + "="*60)
        print(digest)
        print("="*60)
        return
    
    # 查找 openclaw 命令路径
    openclaw_path = shutil.which('openclaw')
    if not openclaw_path:
        # 尝试常见路径
        for path in ['/home/admin/.local/share/pnpm/openclaw', '/usr/local/bin/openclaw', '/usr/bin/openclaw']:
            if os.path.exists(path):
                openclaw_path = path
                break
    
    if not openclaw_path:
        print("错误：找不到 openclaw 命令")
        print("\n" + "="*60)
        print(digest)
        print("="*60)
        return
    
    try:
        # 使用 openclaw 消息命令 - 写入临时文件并使用 --media
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write(digest)
            tmp_file = f.name
        
        cmd = [openclaw_path, 'message', 'send', '--channel', 'dingtalk', '--target', channel, '--media', tmp_file]
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(f"日报已发送至 {channel}")
        os.unlink(tmp_file)
    except subprocess.CalledProcessError as e:
        # 命令执行失败，可能是环境问题，尝试使用 curl 调用 gateway API
        print(f"openclaw 命令执行失败，尝试使用 gateway API...")
        try:
            import urllib.request
            import json
            
            # 读取 gateway URL 和 token
            gateway_url = os.environ.get('OPENCLAW_GATEWAY_URL', 'http://localhost:10845')
            gateway_token = os.environ.get('OPENCLAW_GATEWAY_TOKEN', '5cc41287795243acac103ea8a4aab760')
            
            # 构建请求 - 使用 Gateway tools/invoke API
            url = f"{gateway_url}/tools/invoke"
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {gateway_token}' if gateway_token else ''
            }
            data = {
                'tool': 'message',
                'action': 'send',
                'args': {
                    'channel': 'dingtalk',
                    'target': channel,
                    'message': digest
                }
            }
            
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                headers=headers,
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                if result.get('ok'):
                    print(f"日报已通过 API 发送至 {channel}")
                else:
                    print(f"API 发送失败: {result}")
        except Exception as api_e:
            print(f"API 发送也失败了: {api_e}")
            print(f"\n原始错误: {e}")
            print(f"stdout: {e.stdout.decode() if e.stdout else ''}")
            print(f"stderr: {e.stderr.decode() if e.stderr else ''}")
            print("\n" + "="*60)
            print(digest)
            print("="*60)
    except Exception as e:
        print(f"发送通知失败: {e}")
        print("\n" + "="*60)
        print(digest)
        print("="*60)


def main():
    parser = argparse.ArgumentParser(description='GitHub 热门项目日报获取器')
    parser.add_argument('--notify', action='store_true', help='获取后发送通知')
    parser.add_argument('--channel', type=str, help='通知频道 ID')
    parser.add_argument('--output', type=str, help='输出文件路径')
    args = parser.parse_args()
    
    print("正在获取 GitHub 热门数据...")
    
    # 获取所有分类
    print("  - 最热门项目...")
    hottest = fetch_most_starred()
    
    print("  - 增长最快...")
    trending = fetch_fastest_growing()
    
    print("  - AI/ML 项目...")
    ai_ml = fetch_ai_ml_projects()
    
    # 格式化日报
    digest = format_digest(hottest, trending, ai_ml)
    
    # 自动保存到 output 目录
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(os.path.dirname(script_dir), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    from datetime import datetime
    date_str = datetime.now().strftime('%Y-%m-%d')
    auto_output = os.path.join(output_dir, f'digest-{date_str}.md')
    
    with open(auto_output, 'w', encoding='utf-8') as f:
        f.write(digest)
    print(f"日报已保存至 {auto_output}")
    
    # 如果指定了额外的输出路径，也保存到那里
    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(digest)
        print(f"日报已保存至 {args.output}")
    
    if args.notify or args.channel:
        send_notification(digest, args.channel)
    else:
        print("\n" + digest)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())