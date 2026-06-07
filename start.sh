#!/bin/bash
cd "$(dirname "$0")"

# launchd 环境 PATH 很窄，手动补全
export PATH="/Users/edward/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

BOT=${1:-huapishe}
ENV_FILE=".env.${BOT}"

if [ ! -f "$ENV_FILE" ]; then
    echo "❌ 找不到配置文件: $ENV_FILE"
    echo "可用的 bot: huapishe, badminton"
    exit 1
fi

# 直接指向各自的 env 文件，不再共享 .env（避免多 bot 同时启动的竞态）
export BOT_ENV_FILE="$(pwd)/$ENV_FILE"
echo "🚀 启动 bot: $BOT"
echo "   配置文件: $BOT_ENV_FILE"
exec .venv/bin/python3 main.py
