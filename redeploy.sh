#!/bin/bash
# 重启 lark-claudecode 的两个 bot（改完代码/配置后执行使其生效）。
# 停 → 拉起 → 验证 WebSocket 连接。
set -u
DIR="$(cd "$(dirname "$0")" && pwd)"
LA="$HOME/Library/LaunchAgents"
UID_NUM="$(id -u)"
BOTS=(huapishe badminton)

echo "== 停止 =="
for b in "${BOTS[@]}"; do
    launchctl bootout "gui/$UID_NUM/com.lark-claude.$b" 2>/dev/null && echo "  停 $b" || echo "  $b 未在运行"
done
pkill -f "lark-claudecode/main.py" 2>/dev/null
sleep 2

echo "== 启动 =="
for b in "${BOTS[@]}"; do
    if [ ! -f "$LA/com.lark-claude.$b.plist" ]; then
        echo "  ❌ 缺少 plist: $LA/com.lark-claude.$b.plist"
        continue
    fi
    launchctl bootstrap "gui/$UID_NUM" "$LA/com.lark-claude.$b.plist" && echo "  启 $b"
done
sleep 6

echo "== 验证 =="
launchctl list | grep lark-claude
for b in "${BOTS[@]}"; do
    if tail -n 25 "$DIR/logs/$b.log" 2>/dev/null | grep -q "connected to wss"; then
        echo "  ✅ $b 已连接 Lark"
    else
        echo "  ⚠️  $b 未见连接，查 logs/$b.log 与 logs/$b.boot.log"
    fi
done
