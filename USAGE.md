# 使用说明

在 Lark / 飞书里和本机 Claude Code 对话，并管理两个常驻 bot。

## 一、在 Lark 里聊天（主要用法）

直接发普通消息即与 Claude Code 对话。输入 `/` 弹出按钮菜单，也可手敲命令。

### 后端切换（Provider）

| 命令 | 作用 |
|------|------|
| `/provider` | 查看当前后端 + 按钮切换 |
| `/provider mimo` | 切到小米 MiMo API（自动开新 session，模型固定 `mimo-v2.5-pro`） |
| `/provider anthropic` | 切回 Claude Max/Pro 订阅（用 `/model` 设的模型） |

> 订阅额度耗尽时切 `mimo` 顶上。切换会**自动开启新 session**——两端历史格式不兼容
> （MiMo 返回的 thinking 块 signature 为空，复用旧历史会触发 400）。旧会话仍可 `/resume` 找回。

### 会话管理

| 命令 | 作用 |
|------|------|
| `/new` / `/clear` | 开新 session |
| `/new plan` | 新 session 并进入 Plan 模式 |
| `/resume` | 列出历史 session（按钮选择） |
| `/resume 3` | 恢复第 3 个 session |
| `/stop` | 停止正在运行的任务 |
| `/status` | 当前 session 信息（含后端、模型、目录） |

### 模型与模式

| 命令 | 作用 |
|------|------|
| `/model opus` / `sonnet` / `haiku` | 切换模型（仅订阅后端生效；MiMo 模型固定） |
| `/mode bypass` | 跳过所有确认（默认） |
| `/mode plan` | 只规划不执行 |
| `/mode accept` | 自动接受文件编辑 |
| `/mode default` | 每次工具调用需确认 |

### 工作目录

| 命令 | 作用 |
|------|------|
| `/cd ~/project` | 切换工作目录 |
| `/ls [路径]` | 查看目录内容 |
| `/ws save <名> <路径>` | 保存命名工作空间 |
| `/ws use <名>` | 绑定当前会话到工作空间 |
| `/ws list` / `/ws remove <名>` | 列出 / 删除工作空间 |

### 信息查询

| 命令 | 作用 |
|------|------|
| `/usage` | Claude Max 用量与重置时间 |
| `/skills` | 已安装的 Claude Skills |
| `/mcp` | 已配置的 MCP Servers |
| `/help` | 帮助 |

未注册的斜杠命令（如 `/commit`、`/review`）直接转发给 Claude CLI 执行。

### 其他

- 群聊需 **@机器人** 才响应；不 @ 的消息静默忽略
- 直接发**截图**，Claude 会自动下载并分析

---

## 二、运维（Mac 终端）

项目位置：`~/Claude/Projects/lark-claudecode`

```bash
# 状态 / 进程
launchctl list | grep lark-claude
ps aux | grep main.py | grep -v grep

# 日志（排查首选）
tail -f ~/Claude/Projects/lark-claudecode/logs/huapishe.log
tail -f ~/Claude/Projects/lark-claudecode/logs/badminton.log

# 重启某个 bot（改代码 / .env 后必须重启才生效）
launchctl bootout   gui/$(id -u)/com.lark-claude.huapishe
launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.lark-claude.huapishe.plist
# badminton 同理替换名字

# 手动前台运行（调试）
cd ~/Claude/Projects/lark-claudecode
./start.sh huapishe          # 或 badminton
```

两个 bot 由 launchd 守护（`KeepAlive`），崩溃会自动拉起。

---

## 三、两个 bot 对照

| bot | Lark App | 回调端口 | 默认工作目录 |
|-----|----------|---------|-------------|
| huapishe（画皮师） | `cli_aa9159…` | 9981 | `~/Claude/Projects/manga_workflow` |
| badminton（来一球） | `cli_aa915a…` | 9982 | `~/Claude/Projects/badminton app` |

> 每个 bot 经 `BOT_ENV_FILE` 加载各自的 `.env.<bot>`，互不干扰（不再共享 `.env`）。

---

## 四、新增 bot

1. 在 [Lark 开放平台](https://open.larksuite.com/app) 创建应用，拿到 App ID / Secret
2. 复制一份 `.env.example` 为 `.env.<新名>`，填好凭证、`DEFAULT_CWD`、`CALLBACK_PORT`（错开端口）
3. 仿照 `com.lark-claude.huapishe.plist` 建一份新 plist，指向 `start.sh <新名>`
4. `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.lark-claude.<新名>.plist`

## 五、配置 MiMo 后端

在对应 `.env.<bot>` 填入 `MIMO_API_KEY`（其余 MiMo 变量见 `.env.example`，有默认值），
重启 bot 后即可在 Lark 用 `/provider mimo` 切换。
