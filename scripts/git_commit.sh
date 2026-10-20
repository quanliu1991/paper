#!/bin/bash
# git_commit.sh — 每日任务提交辅助
# 背景：Cursor shell 集成会给命令行中的 git commit 注入 --trailer（旧版 git 不支持），
# 通过脚本内执行可绕过。每日任务统一用本脚本提交。
#
# 用法:
#   bash scripts/git_commit.sh "commit message"     # 参数直接传 message
#   bash scripts/git_commit.sh -F <file>            # 从文件读 message（Windows PowerShell
#                                                   #   调用时中文参数会因 GBK/UTF-8 编码
#                                                   #   丢失，走文件最稳；macOS 不受影响）
set -e
cd "$(dirname "$0")/.."
# 跨平台：macOS 有 /usr/bin/git；Windows Git Bash 无此路径，退回 PATH 中的 git
GIT=/usr/bin/git
command -v "$GIT" >/dev/null 2>&1 || GIT=git

if [ "${1:-}" = "-F" ]; then
  MSGFILE="${2:?usage: git_commit.sh -F <message file>}"
  [ -f "$MSGFILE" ]
  "$GIT" add -A
  "$GIT" commit -F "$MSGFILE" || true
else
  MSG="${1:?usage: git_commit.sh <message> | -F <file>}"
  "$GIT" add -A
  "$GIT" commit -m "$MSG" || true
fi
