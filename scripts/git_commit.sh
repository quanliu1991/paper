#!/bin/bash
# git_commit.sh — 每日任务提交辅助
# 背景：Cursor shell 集成会给命令行中的 git commit 注入 --trailer（旧版 git 不支持），
# 通过脚本内执行可绕过。每日任务统一用本脚本提交。
#
# 用法: bash scripts/git_commit.sh "commit message"
set -e
cd "$(dirname "$0")/.."
MSG="${1:?usage: git_commit.sh <message>}"
/usr/bin/git add -A
/usr/bin/git commit -m "$MSG" || true
