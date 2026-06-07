"""_retry_with_backoff：额度耗尽(99991403)不重试，瞬时错误才重试。"""

import asyncio
import os
import sys

os.environ.setdefault("FEISHU_APP_ID", "test_app_id")
os.environ.setdefault("FEISHU_APP_SECRET", "test_app_secret")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from feishu_client import FeishuClient


def _client():
    return FeishuClient(client=None, app_id="x", app_secret="y")


def test_quota_error_not_retried():
    c = _client()
    calls = {"n": 0}

    async def failing():
        calls["n"] += 1
        raise RuntimeError("发送卡片消息失败: 99991403 This month's API call quota has been exceeded")

    async def run():
        try:
            await c._retry_with_backoff(failing, max_retries=3, initial_delay=0)
        except RuntimeError:
            pass

    asyncio.run(run())
    assert calls["n"] == 1  # 额度错误只尝试一次，不浪费额度重试


def test_transient_error_retried():
    c = _client()
    calls = {"n": 0}

    async def failing():
        calls["n"] += 1
        raise RuntimeError("temporary network glitch")

    async def run():
        try:
            await c._retry_with_backoff(failing, max_retries=3, initial_delay=0)
        except RuntimeError:
            pass

    asyncio.run(run())
    assert calls["n"] == 4  # 首次 + 3 次重试


def test_success_returns_value():
    c = _client()

    async def ok():
        return "done"

    assert asyncio.run(c._retry_with_backoff(ok, initial_delay=0)) == "done"
