#!/bin/bash
# git_push.sh — 每日任务推送辅助（SSH over 443，绕过 22 端口限制与凭证问题）
# 用法: bash scripts/git_push.sh
set -e
cd "$(dirname "$0")/.."
/usr/bin/git push origin main || (/usr/bin/git pull --rebase origin main && /usr/bin/git push origin main)
