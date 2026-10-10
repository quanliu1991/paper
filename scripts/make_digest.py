#!/usr/bin/env python3
"""make_digest.py — 生成月度 digest 草稿 + 清理超期 daily 文件。

用法:
    python3 scripts/make_digest.py --month 2026-10   # 生成 2026 年 10 月 digest 草稿
    python3 scripts/make_digest.py --month 2026-10 --clean  # 同时清理 daily/ 中 >90 天的速览

输出: digest/2026-10-draft.md（草稿，Agent 润色后另存 digest/2026-10.md）
数据源: topics/inference/papers.md 的当月条目 + daily/ 当月速览统计 + data/index.json

清理: daily/ 下文件名日期距今 >90 天的 .md 打印清单（--clean 时执行 git rm）。
"""
import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIGEST_DIR = ROOT / "digest"
DAILY_DIR = ROOT / "daily"
INFERENCE_ARCHIVE = ROOT / "topics" / "inference" / "papers.md"
INDEX_PATH = ROOT / "data" / "index.json"

KEEP_DAYS = 90

ENTRY_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2}) · (.+?)\s*(?:⭐)?\s*$", re.M)
META_RE = re.compile(r"^> .*$", re.M)


def parse_archive(month: str):
    """解析 inference 归档当月条目：[(date, title, meta_line, body_head)]"""
    text = INFERENCE_ARCHIVE.read_text(encoding="utf-8")
    entries = []
    blocks = re.split(r"(?=^### )", text, flags=re.M)
    for b in blocks:
        m = re.match(r"### (\d{4}-\d{2}-\d{2}) · (.+)", b)
        if not m or not m.group(1).startswith(month):
            continue
        meta = re.search(r"^> (.+)$", b, re.M)
        body = b.split("\n", 2)[2].strip() if len(b.split("\n", 2)) > 2 else ""
        entries.append((m.group(1), m.group(2).replace("⭐", "").strip(), meta.group(1) if meta else "", body[:300]))
    # 当月内按日期倒序
    entries.sort(key=lambda x: x[0], reverse=True)
    return entries


def month_stats(month: str):
    """daily/ 当月速览统计：篇数/infra 篇数。"""
    yy, mm = month.split("-")
    pat = DAILY_DIR / yy / mm
    days, total, infra = 0, 0, 0
    for f in pat.glob("*.md"):
        days += 1
        head = f.read_text(encoding="utf-8")[:400]
        t = re.search(r"收录 (\d+) 篇", head)
        i = re.search(r"推理 Infra (\d+) 篇|infra (\d+) 篇", head, re.I)
        if t:
            total += int(t.group(1))
        if i:
            infra += int(i.group(1) or i.group(2))
    return days, total, infra


def stale_daily_files():
    """列出 daily/ 中超期（>KEEP_DAYS 天）文件。"""
    cutoff = dt.date.today() - dt.timedelta(days=KEEP_DAYS)
    stale = []
    for f in DAILY_DIR.glob("*/*/*.md"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})\.md", f.name)
        if m and dt.date.fromisoformat(m.group(1)) < cutoff:
            stale.append(f)
    return stale


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", required=True, help="YYYY-MM")
    ap.add_argument("--clean", action="store_true", help="删除超期 daily 文件（git rm）")
    args = ap.parse_args()
    month = args.month

    entries = parse_archive(month)
    days, total, infra = month_stats(month)

    lines = [f"# 月度回顾 · {month}（草稿）", ""]
    lines.append(f"> 当月速览 {days} 天 · 收录约 {total} 篇 · 推理 Infra 归档 {len(entries)} 篇")
    lines.append("")
    lines.append("## Infra 精选（当月归档全量，按日期倒序）")
    lines.append("")
    for date, title, meta, body in entries:
        lines.append(f"### {date} · {title}")
        lines.append(f"> {meta}")
        lines.append("")
        lines.append(body + ("…" if len(body) >= 300 else ""))
        lines.append("")
    lines.append("## 子方向趋势（Agent 润色时补充）")
    lines.append("")
    lines.append("## 新术语（Agent 从 glossary 当月新增中提取）")
    lines.append("")

    DIGEST_DIR.mkdir(exist_ok=True)
    out = DIGEST_DIR / f"{month}-draft.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"[digest] 草稿 -> {out}（{len(entries)} 条归档）")
    print("[digest] Agent 下一步：润色为最终版 digest/%s.md，补趋势与术语节" % month)

    stale = stale_daily_files()
    if stale:
        print(f"[clean] 超期 daily 文件 {len(stale)} 个：")
        for f in stale:
            print("   ", f.relative_to(ROOT))
        if args.clean:
            for f in stale:
                subprocess.run(["/usr/bin/git", "rm", "-q", str(f.relative_to(ROOT))], cwd=ROOT, check=False)
            print("[clean] 已 git rm（git 历史仍可查：git show HEAD~1:daily/...）")
    else:
        print(f"[clean] 无超期（> {KEEP_DAYS} 天）daily 文件")
    return 0


if __name__ == "__main__":
    sys.exit(main())
