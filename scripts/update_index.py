#!/usr/bin/env python3
"""update_index.py — 从各日 pending JSON 重建 data/index.json（去重索引）。

用法:
    python3 scripts/update_index.py

读取 data/pending/*.json，按 arXiv ID 去重汇总（后写的日期覆盖先写的同 ID 记录，
因为 pending 文件按日期命名、处理顺序即时间序，覆盖后保留最新 metadata）。
仅在每日任务汇总或人工校正时运行；日常去重由 fetch_papers.py 读 index 完成。
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PENDING_DIR = ROOT / "data" / "pending"
INDEX_PATH = ROOT / "data" / "index.json"


def main() -> int:
    if not PENDING_DIR.exists():
        print("no pending dir")
        return 1
    papers = {}
    if INDEX_PATH.exists():
        with open(INDEX_PATH, encoding="utf-8") as f:
            papers = json.load(f).get("papers", {})
    for pf in sorted(PENDING_DIR.glob("*.json")):
        with open(pf, encoding="utf-8") as f:
            d = json.load(f)
        for p in d.get("papers", []):
            pid = p.get("arxiv_id")
            if not pid:
                continue
            papers[pid] = {
                "title": p.get("title", ""),
                "date_added": d.get("date", ""),
                "source": p.get("source", ""),
                "upvotes": p.get("upvotes", 0),
                "reasoning_hit": p.get("reasoning_hit", False),
                "arxiv_url": p.get("arxiv_url", ""),
            }
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump({"papers": papers}, f, ensure_ascii=False, indent=1)
    print(f"[index] {len(papers)} papers indexed -> {INDEX_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
