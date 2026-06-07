"""
Provider 定义：在 Claude Max/Pro 订阅与小米 MiMo API 之间自由切换。

- anthropic：走 claude CLI 自带登录（Max/Pro 订阅），不注入任何环境变量，
  使用 session 里设置的模型（opus / sonnet / haiku）。
- mimo：注入 ANTHROPIC_BASE_URL + ANTHROPIC_API_KEY 指向 MiMo 端点，
  强制使用 MiMo 模型，并关闭扩展思考（MiMo 返回的 thinking 块 signature 为空，
  跨 provider 复用历史会触发 400，故切换时应配合开新 session）。
"""

from bot_config import (
    DEFAULT_PROVIDER,
    MIMO_API_KEY,
    MIMO_BASE_URL,
    MIMO_MODEL,
)

PROVIDERS: dict[str, dict] = {
    "anthropic": {
        "label": "Anthropic 订阅",
        "env": {},          # 不注入，复用 claude CLI 登录凭证
        "model": None,      # None 表示沿用 session 模型
        "disable_thinking": False,
    },
    "mimo": {
        "label": "MiMo",
        "env": {
            "ANTHROPIC_BASE_URL": MIMO_BASE_URL,
            "ANTHROPIC_API_KEY": MIMO_API_KEY,
        },
        "model": MIMO_MODEL,    # 强制 MiMo 模型，忽略 session 模型
        "disable_thinking": True,
    },
}

# 切换 provider 时需要从子进程环境里清掉的覆盖键，保证基线干净。
PROVIDER_ENV_KEYS = ("ANTHROPIC_BASE_URL", "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN")


def get_provider(name: str | None) -> dict:
    """返回 provider 配置；未知名回退到默认 provider。"""
    return PROVIDERS.get(name or DEFAULT_PROVIDER, PROVIDERS[DEFAULT_PROVIDER])


def provider_label(name: str | None) -> str:
    return get_provider(name)["label"]


def is_available(name: str) -> bool:
    """provider 是否可用（mimo 需配置了 API key）。"""
    if name not in PROVIDERS:
        return False
    if name == "mimo":
        return bool(MIMO_API_KEY)
    return True
