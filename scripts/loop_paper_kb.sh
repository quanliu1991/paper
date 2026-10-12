#!/usr/bin/env bash
# paper_kb 每日 21:00 唤醒循环（供 Cursor 监控 shell 使用）
# 用法（在 Cursor 终端后台运行，配合 notify_on_output 正则 ^AGENT_LOOP_TICK_paper_kb）:
#   bash scripts/loop_paper_kb.sh
# 说明: 机器重启后本进程会消失；重新运行上面这条命令即可。漏掉的日期由
# .cursor/prompts/daily-paper.md 步骤 1 自动补齐。
while true; do
  now=$(date +%s)
  target=$(date -v21H -v0M -v0S +%s)
  if [ "$target" -le "$now" ]; then
    target=$(date -v+1d -v21H -v0M -v0S +%s)
  fi
  sleep $((target - now))
  echo 'AGENT_LOOP_TICK_paper_kb {"prompt":"执行 .cursor/prompts/daily-paper.md 每日任务（从 daily/ 最新日期的下一天开始补齐缺失日期，含今天），完成后简报并提交推送。"}'
done
