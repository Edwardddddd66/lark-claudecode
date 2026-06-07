#!/bin/bash
# 在终端用 MiMo token plan 跑 claude。项目无关：cd 到任意项目目录后执行即可，
# 会在当前目录开一个走 MiMo 的 claude 会话（不消耗 Claude 订阅额度）。
#   例：cd ~/Claude/Projects/manga_workflow && ~/Claude/Projects/lark-claudecode/claude-mimo.sh
#       cd "~/Claude/Projects/badminton app" && ~/Claude/Projects/lark-claudecode/claude-mimo.sh
DIR="$(cd "$(dirname "$0")" && pwd)"
# MiMo 配置在 .env.huapishe / .env.badminton 中一致，任取其一读取（只取 MIMO_ 变量）
ENV_FILE="$DIR/.env.huapishe"

_get() { grep -E "^$1=" "$ENV_FILE" | head -1 | cut -d= -f2-; }

export ANTHROPIC_BASE_URL="$(_get MIMO_BASE_URL)"
export ANTHROPIC_API_KEY="$(_get MIMO_API_KEY)"
export MAX_THINKING_TOKENS=0   # MiMo 不支持 Claude thinking 格式

MODEL="$(_get MIMO_MODEL)"; MODEL="${MODEL:-mimo-v2.5-pro}"

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "❌ 未在 $ENV_FILE 找到 MIMO_API_KEY" >&2
    exit 1
fi

exec claude --model "$MODEL" "$@"
