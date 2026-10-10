#!/usr/bin/env python3
"""merge_rearchive.py — 把 data/pending/rearchive-YYYY-MM-DD.md 合并进 topics/inference/papers.md。

按 8 个子方向分节、节内按日期倒序（同日按 upvotes 降序）插入。
可重复运行（幂等）：以 arXiv ID 去重，已存在的条目跳过。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGET = ROOT / "topics" / "inference" / "papers.md"
SRC_DIR = ROOT / "data" / "pending"

SUBTOPIC_MAP = {
    "serving-system": "Serving 系统",
    "kv-cache": "KV Cache 与显存",
    "speculative-decoding": "投机解码",
    "quantization-compression": "量化与压缩",
    "parallelism-scheduling": "并行与调度",
    "moe-inference": "MoE 推理",
    "long-context-vlm": "长上下文与 VLM",
    "inference-other": "Others",
}

ENTRY_RE = re.compile(r"^### (\d{4}-\d{2}-\d{2}) · (.+)$")
SUB_RE = re.compile(r"子方向:\s*(\S+)")
URL_RE = re.compile(r"arxiv\.org/abs/([\w.\-]+)")


def parse_entries(path: Path):
    """返回 [(date, upvotes, subtopic_id, arxiv_id, entry_text)]"""
    entries = []
    lines = path.read_text(encoding="utf-8").splitlines()
    i = 0
    while i < len(lines):
        m = ENTRY_RE.match(lines[i])
        if not m:
            i += 1
            continue
        date, title = m.group(1), m.group(2)
        block = [lines[i]]
        i += 1
        while i < len(lines) and not ENTRY_RE.match(lines[i]) and not lines[i].startswith("# "):
            block.append(lines[i])
            i += 1
        text = "\n".join(block).rstrip()
        sub_m = SUB_RE.search(text)
        url_m = URL_RE.search(text)
        up_m = re.search(r"upvotes:\s*(\d+)", text)
        if sub_m and url_m:
            entries.append((
                date,
                int(up_m.group(1)) if up_m else 0,
                sub_m.group(1).rstrip("· "),
                url_m.group(1),
                text,
            ))
    return entries


def main() -> int:
    if not TARGET.exists():
        print("target missing", file=sys.stderr)
        return 1
    existing_ids = set(URL_RE.findall(TARGET.read_text(encoding="utf-8")))

    new_entries = []
    for src in sorted(SRC_DIR.glob("rearchive-*.md")):
        for e in parse_entries(src):
            if e[3] in existing_ids:
                continue
            new_entries.append(e)
            existing_ids.add(e[3])

    if not new_entries:
        print("[merge] 无新增条目")
        return 0

    # 读入目标文件，逐子方向插入
    sections = {}
    lines = TARGET.read_text(encoding="utf-8").splitlines(keepends=True)
    header_end = 0
    sec_positions = {}  # subtopic_id -> 起始行号
    for idx, ln in enumerate(lines):
        if ln.startswith("## ") and ln.strip("## \n") in SUBTOPIC_MAP.values():
            # 记录小节标题行
            for sid, name in SUBTOPIC_MAP.items():
                if name == ln.strip("## \n"):
                    sec_positions[sid] = idx
        if ln.startswith("## ") and header_end == 0:
            header_end = idx  # 第一个 ## 之前是文件头

    # 组织新条目: subtopic -> list，按 (date desc, upvotes desc)
    from collections import defaultdict
    by_sub = defaultdict(list)
    for e in new_entries:
        by_sub[e[2]].append(e)
    for sid in by_sub:
        by_sub[sid].sort(key=lambda x: (x[0], x[1]), reverse=True)

    # 从后往前插入，避免行号位移
    for sid in sorted(sec_positions, key=lambda s: -sec_positions[s]):
        if sid not in by_sub:
            continue
        insert_at = sec_positions[sid] + 1  # 标题行之后
        block = "".join(e[4] + "\n\n" for e in by_sub[sid])
        lines.insert(insert_at, "\n" + block)

    TARGET.write_text("".join(lines), encoding="utf-8")
    print(f"[merge] 插入 {len(new_entries)} 条到 {TARGET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
