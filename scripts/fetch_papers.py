#!/usr/bin/env python3
"""fetch_papers.py — 每日论文抓取（HuggingFace Daily Papers + arXiv 关键词订阅）

用法:
    python3 scripts/fetch_papers.py --date 2026-10-09        # 抓取指定日期
    python3 scripts/fetch_papers.py                           # 默认今天

输出: data/pending/YYYY-MM-DD.json （待 Agent 分析的论文清单）
已收录论文记录在 data/index.json（arXiv ID 去重主键），命中的不再输出。

纯 Python 标准库实现（urllib + xml.etree + json），无需 pip install。
"""
import argparse
import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

try:
    import yaml
except ImportError:  # pyyaml 缺失时用内置简易解析不现实，直接报错提示
    print("ERROR: 需要 pyyaml：pip3 install pyyaml", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "config" / "keywords.yaml"
INDEX_PATH = ROOT / "data" / "index.json"
PENDING_DIR = ROOT / "data" / "pending"

HF_API = "https://huggingface.co/api/daily_papers?date={date}"
ARXIV_API = "https://export.arxiv.org/api/query"
ATOM_NS = "{http://www.w3.org/2005/Atom}"
ARXIV_NS = "{http://arxiv.org/schemas/atom}"

UA = "paper-kb/1.0 (daily research digest; +https://github.com/quanliu1991/paper)"


def http_get(url: str, timeout: int = 30) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def load_config() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_index() -> dict:
    if INDEX_PATH.exists():
        with open(INDEX_PATH, encoding="utf-8") as f:
            return json.load(f)
    return {"papers": {}}


def arxiv_id_from_url(url: str) -> str:
    # https://huggingface.co/papers/2610.08077 -> 2610.08077
    m = re.search(r"(\d{4}\.\d{4,6})(v\d+)?$", url.strip())
    return m.group(1) if m else url.strip("/").split("/")[-1]


def hit_reasoning(text: str, keywords: list) -> bool:
    """标题/摘要是否命中关键词表（通用子串匹配，供 infra_hit 等使用）。"""
    low = text.lower()
    return any(k.lower() in low for k in keywords)


# ---------------------------------------------------------------- HuggingFace
def fetch_hf_daily(date: str) -> list:
    """HF Daily Papers：自带 upvotes（社区热度信号）。"""
    papers = []
    try:
        raw = http_get(HF_API.format(date=date))
        items = json.loads(raw)
    except Exception as e:
        print(f"  [warn] HF API 失败: {e}", file=sys.stderr)
        return papers
    for it in items:
        p = it.get("paper", {})
        pid = p.get("id") or arxiv_id_from_url(p.get("url", ""))
        if not pid:
            continue
        authors = ", ".join(a.get("name", "") for a in (p.get("authors") or [])[:6])
        papers.append({
            "arxiv_id": pid,
            "title": re.sub(r"\s+", " ", (p.get("title") or "").strip()),
            "authors": authors,
            "abstract": (p.get("summary") or "").strip(),
            "upvotes": it.get("paper", {}).get("upvotes") or it.get("upvotes") or 0,
            "url": f"https://huggingface.co/papers/{pid}",
            "arxiv_url": f"https://arxiv.org/abs/{pid}",
            "source": "hf_daily",
        })
    return papers


# ---------------------------------------------------------------- arXiv
def fetch_arxiv(cfg: dict, date: str) -> list:
    """arXiv API 关键词订阅：所有关键词合并为一次 OR 查询（按提交日期倒序）。

    日期窗口 ±1 天（arXiv 索引有延迟），重复论文由 data/index.json 去重兜底。
    """
    target = dt.date.fromisoformat(date)
    win_start = dt.datetime(target.year, target.month, target.day, tzinfo=dt.timezone.utc) - dt.timedelta(days=1)
    win_end = dt.datetime(target.year, target.month, target.day, tzinfo=dt.timezone.utc) + dt.timedelta(days=2)

    keywords = cfg.get("arxiv_keywords", [])
    cats = cfg.get("arxiv_categories", [])
    max_results = min(int(cfg.get("arxiv_max_per_query", 15)) * max(len(keywords), 1), 100)

    # 手动拼 URL：arXiv API 用 + 表示空格/布尔 OR；引号需转义为 %22
    # 用 submittedDate 范围过滤，保证回填旧日期时能命中当天窗口的论文
    range_part = (
        "submittedDate:["
        + win_start.strftime("%Y%m%d%H%M")
        + "+TO+"
        + win_end.strftime("%Y%m%d%H%M")
        + "]"
    )
    kw_part = "+OR+".join("all:%22" + k.replace(" ", "+") + "%22" for k in keywords)
    query = f"({kw_part})"
    if cats:
        cat_part = "+OR+".join(f"cat:{c}" for c in cats)
        query += f"+AND+({cat_part})"
    query += f"+AND+{range_part}"
    url = f"{ARXIV_API}?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"

    papers, seen = [], set()
    try:
        raw = http_get(url)
        root = ET.fromstring(raw)
    except Exception as e:
        print(f"  [warn] arXiv API 失败: {e}", file=sys.stderr)
        return papers

    for entry in root.findall(f"{ATOM_NS}entry"):
        pid_el = entry.find(f"{ATOM_NS}id")
        if pid_el is None:
            continue
        m = re.search(r"abs/([\w.\-]+)(v\d+)?$", pid_el.text or "")
        if not m:
            continue
        pid = m.group(1)
        if pid in seen:
            continue
        seen.add(pid)
        pub_el = entry.find(f"{ATOM_NS}published")
        try:
            pub = dt.datetime.fromisoformat((pub_el.text or "").replace("Z", "+00:00"))
        except Exception:
            continue
        if not (win_start <= pub < win_end):
            continue
        title_el = entry.find(f"{ATOM_NS}title")
        sum_el = entry.find(f"{ATOM_NS}summary")
        authors = ", ".join(
            (a.findtext(f"{ATOM_NS}name") or "")
            for a in entry.findall(f"{ATOM_NS}author")[:6]
        )
        text = f"{title_el.text or ''} {sum_el.text or ''}".lower()
        hit_kws = [k for k in keywords if k.lower() in text]
        papers.append({
            "arxiv_id": pid,
            "title": re.sub(r"\s+", " ", (title_el.text or "").strip()),
            "authors": authors,
            "abstract": re.sub(r"\s+", " ", (sum_el.text or "").strip()),
            "upvotes": 0,
            "url": f"https://huggingface.co/papers/{pid}",
            "arxiv_url": f"https://arxiv.org/abs/{pid}",
            "source": "arxiv_kw",
            "keyword": ", ".join(hit_kws[:3]),
        })
    return papers


# ---------------------------------------------------------------- 主流程
def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=dt.date.today().isoformat(), help="YYYY-MM-DD")
    args = ap.parse_args()
    date = args.date

    cfg = load_config()
    index = load_index()

    print(f"[fetch] HuggingFace Daily Papers: {date}")
    hf = fetch_hf_daily(date)
    print(f"  -> {len(hf)} 篇")

    print(f"[fetch] arXiv 关键词订阅: {date}")
    ax = fetch_arxiv(cfg, date)
    print(f"  -> {len(ax)} 篇")

    # 限流：arXiv 关键词来源每日最多贡献 N 篇（HF 全保留，社区策展质量高）
    ax_cap = int(cfg.get("arxiv_daily_cap", 30))
    if len(ax) > ax_cap:
        ax = ax[:ax_cap]

    # 合并去重（同 ID 时保留 HF 记录，其 upvotes 更可信）
    merged = {}
    for p in hf + ax:
        pid = p["arxiv_id"]
        if pid not in merged:
            merged[pid] = p
        elif p["source"] == "hf_daily":
            p["keyword"] = merged[pid].get("keyword")
            merged[pid] = p
        else:
            merged[pid]["upvotes"] = merged[pid]["upvotes"] or 0

    known = set(index["papers"].keys())
    infra_kws = cfg.get("infra_keywords", [])
    feat_th = int(cfg.get("featured_threshold_upvotes", 10))

    fresh = []
    for pid, p in merged.items():
        if pid in known:
            continue
        p["infra_hit"] = hit_reasoning(p["title"] + " " + p["abstract"], infra_kws)
        p["featured"] = (p["upvotes"] >= feat_th) or p["infra_hit"]
        fresh.append(p)

    # 排序：精选在前，upvotes 降序，命中 infra 词优先
    fresh.sort(key=lambda x: (not x["featured"], -x["upvotes"], not x["infra_hit"]))

    PENDING_DIR.mkdir(parents=True, exist_ok=True)
    out = PENDING_DIR / f"{date}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump({"date": date, "count": len(fresh), "papers": fresh}, f, ensure_ascii=False, indent=2)

    n_infra = sum(1 for p in fresh if p["infra_hit"])
    print(f"[fetch] 合计 {len(merged)} 篇，去重后新增 {len(fresh)} 篇（命中 infra 推理词 {n_infra} 篇）")
    print(f"[fetch] 待分析清单 -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
