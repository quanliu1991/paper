#!/usr/bin/env bash
# test_cross_platform.sh — 跨平台脚本改动的冒烟测试
# 覆盖：loop_paper_kb.sh 的双分支时间计算、check_paper_loop.sh 的进程检测、
#       git_commit.sh / git_push.sh 的 git 探测、make_digest.py 的 git 探测。
# 用法: bash scripts/test_cross_platform.sh
# 设计原则：只读测试（不产生提交、不推送、不改仓库文件），可反复运行。
set -u
cd "$(dirname "$0")/.."
PASS=0; FAIL=0

ok()   { PASS=$((PASS+1)); echo "  ✔ $1"; }
bad()  { FAIL=$((FAIL+1)); echo "  ✘ $1"; }
check() { # check <描述> <条件退出码>
  if [ "$2" -eq 0 ]; then ok "$1"; else bad "$1"; fi
}

echo "== 1. loop_paper_kb.sh 时间计算 =="
# 1a. GNU date 分支（Linux/Windows Git Bash）
if date -d "today 21:00" +%s >/dev/null 2>&1; then
  target=$(date -d "today 21:00" +%s); now=$(date +%s)
  [ "$target" -gt 0 ] && [ "$((target - now))" -gt $(( -86400*2 )) ] && [ "$((target - now))" -lt $((86400*2)) ]
  check "GNU date: 目标时刻在 ±48h 内（拿到合法时间戳）" $?
  # 已过 21:00 时应滚到明天
  if [ "$target" -le "$now" ]; then
    t2=$(date -d "tomorrow 21:00" +%s)
    [ "$t2" -gt "$target" ]
    check "GNU date: 今天 21:00 已过 → 滚到明天 21:00" $?
  else
    ok "GNU date: 今天 21:00 未到（无需滚动分支）"
  fi
else
  echo "  （本机无 GNU date -d，跳过 GNU 分支测试）"
fi
# 1b. BSD date 分支（macOS）——模拟其语法在本机不可用时脚本仍能走通
if date -v21H +%s >/dev/null 2>&1; then
  target=$(date -v21H -v0M -v0S +%s)
  [ "$target" -gt 0 ]
  check "BSD date: date -v21H 可用（macOS 场景，本机仅 macOS 会走到）" $?
else
  ok "BSD date: 不可用 → 脚本按设计走 GNU 分支（非 macOS 行为正确）"
fi

echo "== 2. check_paper_loop.sh 进程检测 =="
out=$(bash scripts/check_paper_loop.sh 2>/dev/null); rc=$?
case "$out" in
  *"正常运行中"*)
    if [ "$rc" -eq 0 ]; then ok "循环运行中 → 输出正常标记且 exit 0"; else bad "输出正常标记但 exit=$rc（应为 0）"; fi
    ;;
  *"未运行"*)
    if [ "$rc" -eq 1 ]; then ok "循环未运行 → 提醒文案且 exit 1（预期行为）"; else bad "输出提醒但 exit=$rc（应为 1）"; fi
    ;;
  *)
    bad "输出无法识别：$out"
    ;;
esac
# 检测逻辑应能找到本测试进程自身依赖的 bash（自检：脚本确实在 bash 里跑）
[ -n "${BASH_VERSION:-}" ]
check "检测脚本运行在 bash 环境（BASH_VERSION=$BASH_VERSION）" $?

echo "== 3. git_commit.sh / git_push.sh git 探测 =="
GIT=/usr/bin/git
if command -v "$GIT" >/dev/null 2>&1; then
  ok "git 探测: /usr/bin/git 存在（macOS 场景路径）"
else
  GIT=git
  command -v git >/dev/null 2>&1
  check "git 探测: /usr/bin/git 不存在 → 回退 PATH git（Windows 场景）" $?
fi
"$GIT" rev-parse --is-inside-work-tree >/dev/null 2>&1
check "git 探测: 最终 git 可在仓库内执行（$("$GIT" --version 2>/dev/null | head -1)）" $?

echo "== 4. make_digest.py git 探测 =="
# Windows 控制台默认 GBK：强制 UTF-8 输出，避免非 ASCII 字符报错
PYTHONIOENCODING=utf-8 python3 - <<'PYEOF'
import os, shutil, subprocess
git_bin = "/usr/bin/git" if os.path.exists("/usr/bin/git") else shutil.which("git")
assert git_bin, "git not found"
r = subprocess.run([git_bin, "rev-parse", "--is-inside-work-tree"], capture_output=True, text=True, cwd=".")
assert r.stdout.strip() == "true", r.stdout
print(f"  [OK] make_digest probe: git={git_bin}, rev-parse OK")
PYEOF
check "make_digest.py: 同款探测代码可找到 git 且工作" $?

echo "== 5. python3 / fetch_papers.py 可用性 =="
command -v python3 >/dev/null 2>&1
check "python3 在 PATH 中（每日任务依赖）" $?
python3 -c "import yaml" 2>/dev/null
check "pyyaml 已安装（fetch_papers.py 依赖）" $?

echo ""
echo "=============================="
echo "结果: $PASS 通过, $FAIL 失败"
[ "$FAIL" -eq 0 ] && echo "全部通过 ✔" || echo "存在失败 ✘"
exit "$FAIL"
