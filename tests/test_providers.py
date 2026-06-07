"""provider 切换逻辑测试（anthropic 订阅 ↔ MiMo）。"""

import os
import sys

os.environ.setdefault("FEISHU_APP_ID", "test_app_id")
os.environ.setdefault("FEISHU_APP_SECRET", "test_app_secret")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import providers


def test_only_two_providers():
    assert set(providers.PROVIDERS) == {"anthropic", "mimo"}


def test_anthropic_uses_subscription():
    p = providers.get_provider("anthropic")
    assert p["env"] == {}          # 不注入，走 CLI 登录
    assert p["model"] is None      # 沿用 session 模型
    assert p["disable_thinking"] is False


def test_mimo_injects_endpoint_and_forces_model():
    p = providers.get_provider("mimo")
    assert p["model"] == "mimo-v2.5-pro"
    assert p["disable_thinking"] is True
    assert "ANTHROPIC_BASE_URL" in p["env"]
    assert "ANTHROPIC_API_KEY" in p["env"]


def test_unknown_provider_falls_back_to_default():
    default = providers.PROVIDERS[providers.DEFAULT_PROVIDER]
    assert providers.get_provider("nope") is default
    assert providers.get_provider(None) is default


def test_is_available_requires_mimo_key(monkeypatch):
    monkeypatch.setattr(providers, "MIMO_API_KEY", "")
    assert providers.is_available("mimo") is False
    monkeypatch.setattr(providers, "MIMO_API_KEY", "tp-xxx")
    assert providers.is_available("mimo") is True
    assert providers.is_available("anthropic") is True
    assert providers.is_available("nope") is False


def test_provider_label():
    assert providers.provider_label("mimo") == "MiMo"
    assert providers.provider_label("anthropic") == "Anthropic 订阅"
