"""session 里 provider 字段的默认值、持久化、跨新 session 继承。"""

import asyncio
import os
import sys

os.environ.setdefault("FEISHU_APP_ID", "test_app_id")
os.environ.setdefault("FEISHU_APP_SECRET", "test_app_secret")

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot_config import DEFAULT_PROVIDER
from session_store import SessionStore


def test_default_provider():
    store = SessionStore()
    cur = asyncio.run(store.get_current("u", "c"))
    assert cur.provider == DEFAULT_PROVIDER


def test_set_provider_persists():
    store = SessionStore()
    asyncio.run(store.set_provider("u", "c", "mimo"))
    cur = asyncio.run(store.get_current("u", "c"))
    assert cur.provider == "mimo"


def test_new_session_keeps_provider():
    store = SessionStore()
    asyncio.run(store.set_provider("u", "c", "mimo"))
    asyncio.run(store.new_session("u", "c"))
    cur = asyncio.run(store.get_current("u", "c"))
    assert cur.provider == "mimo"  # 切后端后开新 session 仍保留后端
