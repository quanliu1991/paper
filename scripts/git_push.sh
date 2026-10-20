#!/bin/bash
# git_push.sh — 每日任务推送辅助（SSH over 443，绕过 22 端口限制与凭证问题）
# 用法: bash scripts/git_push.sh
set -e
cd "$(dirname "$0")/.."
# 跨平台：macOS 有 /usr/bin/git；Windows Git Bash 无此路径，退回 PATH 中的 git
GIT=/usr/bin/git
command -v "$GIT" >/dev/null 2>&1 || GIT=git
"$GIT" push origin main || ("$GIT" pull --rebase origin main && "$GIT" push origin main)
