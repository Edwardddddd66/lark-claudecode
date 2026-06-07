import os
import shutil
from dotenv import load_dotenv

# 多 bot 部署时通过 BOT_ENV_FILE 指定各自的 env 文件，避免多个进程
# 共享同一个 .env 产生竞态（同时启动会互相覆盖配置）。未设置时回退到 .env。
load_dotenv(os.getenv("BOT_ENV_FILE") or ".env")

FEISHU_APP_ID = os.environ["FEISHU_APP_ID"]
FEISHU_APP_SECRET = os.environ["FEISHU_APP_SECRET"]

# 飞书域名：国内用 open.feishu.cn，国际版用 open.larksuite.com
FEISHU_DOMAIN = os.getenv("FEISHU_DOMAIN", "https://open.feishu.cn")

CLAUDE_CLI = os.getenv("CLAUDE_CLI_PATH") or shutil.which("claude") or "claude"

DEFAULT_MODEL = os.getenv("DEFAULT_MODEL", "claude-opus-4-6")
DEFAULT_CWD = os.path.expanduser(os.getenv("DEFAULT_CWD", "~"))
PERMISSION_MODE = os.getenv("PERMISSION_MODE", "bypassPermissions")

# Provider：anthropic = Claude Max/Pro 订阅（默认，走 CLI 自带登录），
# mimo = 小米 MiMo API（需在 .env 配置 MIMO_API_KEY），可在飞书用 /provider 切换。
DEFAULT_PROVIDER = os.getenv("DEFAULT_PROVIDER", "anthropic")
MIMO_BASE_URL = os.getenv("MIMO_BASE_URL", "https://token-plan-cn.xiaomimimo.com/anthropic")
MIMO_API_KEY = os.getenv("MIMO_API_KEY", "")
MIMO_MODEL = os.getenv("MIMO_MODEL", "mimo-v2.5-pro")

# 每个 bot 按 App ID 独立 session 目录，避免多个 bot 进程共享同一个
# sessions.json 时整份覆写互相冲掉对方的会话/设置数据。
SESSIONS_DIR = os.path.expanduser(f"~/.feishu-claude/{FEISHU_APP_ID}")

# 卡片按钮回调 HTTP 端口（需 ngrok 暴露）
CALLBACK_PORT = int(os.getenv("CALLBACK_PORT", "9981"))

# 流式卡片更新：每积累多少字符推送一次
STREAM_CHUNK_SIZE = int(os.getenv("STREAM_CHUNK_SIZE", "20"))
