#!/usr/bin/env bash
# check_paper_loop.sh — 检查每日论文任务唤醒循环是否存活，挂了就提醒
# 触发时机：Cursor 每次打开本工作区（由 .vscode/tasks.json 自动运行）
# 提醒方式：终端提示音 + 系统通知（macOS 通知中心 / Windows 弹窗）
# 手动自启命令见提醒文案：bash scripts/loop_paper_kb.sh（需在 Cursor 终端后台跑，
#   配合 notify_on_output ^AGENT_LOOP_TICK_paper_kb 唤醒 Agent）
if command -v pgrep >/dev/null 2>&1; then
  if pgrep -f "bash scripts/loop_paper_kb.sh" > /dev/null 2>&1; then
    echo "[paper-kb] 每日 21:00 唤醒循环正常运行中 ✔"
    exit 0
  fi
else
  # Windows Git Bash 无 pgrep：用 tasklist 查 bash 进程的命令行（依赖 WMI 查询）
  if command -v wmic >/dev/null 2>&1; then
    if wmic process where "name='bash.exe'" get commandline 2>/dev/null | grep -q "loop_paper_kb.sh"; then
      echo "[paper-kb] 每日 21:00 唤醒循环正常运行中 ✔"
      exit 0
    fi
  elif command -v powershell >/dev/null 2>&1; then
    if powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"name='bash.exe'\" | Where-Object {\$_.CommandLine -like '*loop_paper_kb.sh*'}" 2>/dev/null | grep -q "loop_paper_kb"; then
      echo "[paper-kb] 每日 21:00 唤醒循环正常运行中 ✔"
      exit 0
    fi
  fi
fi

echo "🔔 [paper-kb] 每日论文任务唤醒循环未运行！重启 Cursor/机器后它会消失。"
echo ""
echo "    手动恢复方法：在 Cursor 终端后台运行（Agent 会收到输出通知）："
echo ""
echo "    bash scripts/loop_paper_kb.sh"
echo ""
# 终端铃声（BEL 同时触发 Cursor 终端提示音）
printf '\a'
# 系统通知：macOS 通知中心 / Windows 弹窗（PowerShell）
if command -v osascript >/dev/null 2>&1; then
  osascript -e 'display notification "每日论文任务循环未运行，请在终端执行: bash scripts/loop_paper_kb.sh" with title "paper-kb 唤醒循环未启动" sound name "Hero"'
elif command -v powershell >/dev/null 2>&1; then
  powershell -NoProfile -Command "[reflection.assembly]::loadwithpartialname('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('每日论文任务循环未运行，请在终端执行: bash scripts/loop_paper_kb.sh','paper-kb 唤醒循环未启动')" >/dev/null 2>&1 &
fi
exit 1
