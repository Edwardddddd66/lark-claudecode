#!/bin/bash
# 在终端用 MiMo token plan 跑 claude（复用本项目 .env.huapishe 里的 MiMo 配置）。
# 用法：cd 到任意项目目录后执行本脚本，会在当前目录开一个走 MiMo 的 claude 会话。
#   例：cd ~/Claude/Projects/manga_workflow && ~/Claude/Projects/lark-claudecode/claude-mimo.sh
DIR="$(cd "$(dirname "$0")" && pwd)"

set -a
# shellcheck disable=SC1090
source "$DIR/.env.huapishe"
set +a

export ANTHROPIC_BASE_URL="$MIMO_BASE_URL"
export ANTHROPIC_API_KEY="$MIMO_API_KEY"
export MAX_THINKING_TOKENS=0   # MiMo 不支持 Claude thinking 格式

exec claude --model "${MIMO_MODEL:-mimo-v2.5-pro}" "$@"
