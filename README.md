# GitHub 热门项目日报

每日自动获取 GitHub 热门开源项目，生成中文日报并推送到指定频道。

## 功能特点

- 📊 **三个分类**：最热门项目、增长最快、AI/ML 相关
- 🇨🇳 **中文输出**：项目描述自动翻译为中文，保留技术术语
- ⏰ **定时推送**：支持 cron 定时任务自动推送
- 🔧 **灵活配置**：支持环境变量和命令行参数

## 快速开始

### 1. 安装依赖

本技能仅依赖 Python 3 标准库，无需额外安装。

### 2. 配置环境变量（可选但推荐）

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的配置
```

### 3. 手动运行测试

```bash
python3 scripts/fetch_trending.py
```

## 详细配置

### GitHub Token（推荐）

获取 GitHub Personal Access Token 以提高 API 限额：

1. 访问 https://github.com/settings/tokens
2. 点击 "Generate new token (classic)"
3. 选择 `public_repo` 权限
4. 复制生成的 token
5. 添加到 `.env` 文件：`GITHUB_TOKEN=your_token_here`

**限额对比：**
- 无 Token：10 次/小时
- 有 Token：5000 次/小时

### 通知频道配置

设置默认推送频道：

```bash
# .env 文件
NOTIFY_CHANNEL=your_channel_id
```

频道 ID 获取方式：
- 钉钉：使用用户 ID 或群聊 ID
- 其他平台：参考对应平台文档

## 使用方式

### 方式一：手动获取并查看

```bash
python3 scripts/fetch_trending.py
```

### 方式二：保存到文件

```bash
python3 scripts/fetch_trending.py --output /path/to/digest.md
```

### 方式三：推送到指定频道

```bash
# 使用命令行参数
python3 scripts/fetch_trending.py --notify --channel <channel_id>

# 或使用环境变量中配置的默认频道
python3 scripts/fetch_trending.py --notify
```

### 方式四：定时自动推送

使用 cron 设置定时任务：

```bash
# 编辑 crontab
crontab -e

# 每天早上 9 点自动推送
0 9 * * * cd /path/to/github-trending-digest && ./scripts/run_daily.sh

# 或每小时推送一次
0 * * * * cd /path/to/github-trending-digest && ./scripts/run_daily.sh
```

## 输出示例

```
# 🔥 GitHub 热门项目日报 - 2026年03月21日

## 📈 最热门项目
最近创建的获得最多星标的项目：

📦 **NVIDIA/NemoClaw**
   在 NVIDIA OpenShell 中安全运行 OpenClaw，提供托管推理服务
   ⭐ 14,290 星标 | 🔤 JavaScript
   🔗 https://github.com/NVIDIA/NemoClaw

📦 **aiming-lab/AutoResearchClaw**
   自主研究代理，从想法到论文
   ⭐ 7,112 星标 | 🔤 Python
   🔗 https://github.com/aiming-lab/AutoResearchClaw

## 🚀 增长最快
近期活跃度最高的项目：
...

## 🤖 人工智能/机器学习
AI/ML 领域的新热门项目：
...
```

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--notify` | 发送通知 | `--notify` |
| `--channel` | 指定频道 ID | `--channel 123456` |
| `--output` | 输出到文件 | `--output /tmp/digest.md` |

## 文件结构

```
github-trending-digest/
├── SKILL.md              # 技能元数据（OpenClaw 使用）
├── README.md             # 本使用说明文档
├── .env.example          # 环境变量示例
├── .env                  # 实际配置文件（需自行创建）
└── scripts/
    ├── fetch_trending.py # 主程序
    └── run_daily.sh      # 定时运行脚本
```

## 数据来源

使用 GitHub Search API 获取数据：
- 最热门：最近创建的星标最多的项目
- 增长最快：近期有推送的高星标项目
- AI/ML：与人工智能、机器学习相关的项目

## 故障排除

### API 速率限制

**现象：** 部分分类显示 "暂无数据"

**解决：** 配置 GitHub Token
```bash
export GITHUB_TOKEN=your_token_here
```

### 推送失败

**现象：** 提示 "发送通知失败"

**检查：**
1. 频道 ID 是否正确
2. OpenClaw 消息功能是否配置
3. 查看详细错误信息
4. Gateway 服务是否运行（端口 10845）
5. 检查 OPENCLAW_GATEWAY_TOKEN 是否正确

### 输出目录

日报会自动保存到：
```
output/digest-YYYY-MM-DD.md
```

### 定时任务配置

OpenClaw Cron 配置 (`~/.openclaw/cron/jobs.json`)：
```json
{
  "id": "github-trending-daily",
  "name": "GitHub Trending Daily Digest",
  "schedule": "0 9 * * *",
  "command": "export NOTIFY_CHANNEL=your_channel_id && export OPENCLAW_GATEWAY_TOKEN=your_token && cd /path/to/github-trending-digest && python3 scripts/fetch_trending.py --notify",
  "enabled": true
}
```

环境变量：
- `NOTIFY_CHANNEL` - 推送目标频道 ID
- `OPENCLAW_GATEWAY_URL` - Gateway 地址（默认 http://localhost:10845）
- `OPENCLAW_GATEWAY_TOKEN` - Gateway 认证 Token
- `GITHUB_TOKEN` - GitHub API Token（可选）

## 更新日志

### v1.0 (2026-03-21)

- ✅ 初始版本发布
- ✅ 支持三个分类：最热门、增长最快、AI/ML
- ✅ 中文描述自动翻译
- ✅ 支持定时推送
- ✅ 完整文档

## 贡献

欢迎提交 Issue 或 PR 改进本技能。

## 许可证

MIT License
