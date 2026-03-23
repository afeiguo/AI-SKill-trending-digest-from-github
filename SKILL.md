---
name: github-trending-digest
description: 每日 GitHub 热门开源项目中文日报 - 获取并汇总 GitHub 上最热门的开源项目。当用户需要每日更新的 GitHub 热门仓库、流行开源项目、增长最快的项目或 AI/ML 相关项目时使用。支持三个分类：最多星标（最热门）、增长最快、AI/ML 相关新项目。
---

# GitHub 热门项目日报

每日获取 GitHub 热门开源项目，生成中文日报，分为三个分类展示。

## 分类

1. **📈 最热门项目** - 最近创建的获得最多星标的项目
2. **🚀 增长最快** - 近期活跃度最高的项目（最近有推送）
3. **🤖 人工智能/机器学习** - AI/ML 领域的新热门项目

## 数据来源

使用 GitHub 搜索 API 获取热门仓库：
- `https://api.github.com/search/repositories`

## 使用方法

### 手动获取

运行脚本获取今日热门项目日报：

```bash
python3 scripts/fetch_trending.py
```

保存到文件：
```bash
python3 scripts/fetch_trending.py --output /tmp/digest.md
```

### 发送到频道

将日报发送到指定频道：

```bash
python3 scripts/fetch_trending.py --notify --channel <频道ID>
```

或设置 `NOTIFY_CHANNEL` 环境变量：

```bash
export NOTIFY_CHANNEL="你的频道ID"
python3 scripts/fetch_trending.py --notify
```

### 定时推送（Cron）

设置定时任务，每天早上 9 点自动推送：

```bash
# 编辑定时任务
crontab -e

# 添加这行，每天早上 9 点推送
0 9 * * * cd /path/to/github-trending-digest && ./scripts/run_daily.sh
```

或直接运行脚本：

```bash
./scripts/run_daily.sh
```

## 配置

在技能目录创建 `.env` 文件：

```bash
# GitHub 个人访问令牌，用于提高 API 调用限额（推荐）
GITHUB_TOKEN=你的_github_token

# 默认通知频道
NOTIFY_CHANNEL=你的频道ID
```

### 获取 GitHub Token

1. 前往 GitHub 设置 → 开发者设置 → 个人访问令牌
2. 生成新的令牌（classic），选择 `public_repo` 权限
3. 复制令牌并添加到 `.env` 文件

没有令牌时，脚本限制为每小时每 IP 10 次请求。

## 输出格式

日报包含每个项目的以下信息：
- 📦 仓库名称和所有者
- 项目描述（自动翻译为中文）
- 🔤 主要编程语言
- ⭐ 星标数量
- 🔗 仓库直达链接

## 示例输出

```
# 🔥 GitHub 热门项目日报 - 2026年03月21日

## 📈 最热门项目
最近创建的获得最多星标的项目：

📦 **owner/repo-name**
   项目描述（中文翻译）
   ⭐ 1,234 星标 | 🔤 Python
   🔗 https://github.com/owner/repo-name

## 🚀 增长最快
...

## 🤖 人工智能/机器学习
...
```

## 故障排除

**"API 速率限制已达上限" 错误：**
- 设置 `GITHUB_TOKEN` 环境变量，可将限额从每小时 10 次提高到 5000 次

**某个分类无数据：**
- 可能是 API 速率限制导致
- 稍后重试或配置 GitHub Token

**脚本运行时间过长：**
- AI/ML 分类会进行多次 API 调用以获取多样化结果
- 这是正常现象，有助于避免触发速率限制
