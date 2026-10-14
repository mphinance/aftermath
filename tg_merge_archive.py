#!/usr/bin/env python3
"""Merge a remote posts_archive.jsonl into the local one, de-duplicated by post id.

Usage:
  rsync -az coolify:/home/mph/apps/aftermath-watch/data/telegram_funnel/posts_archive.jsonl /tmp/remote_archive.jsonl
  python3 tg_merge_archive.py /tmp/remote_archive.jsonl [--local data/telegram_funnel/posts_archive.jsonl] [--dry-run]

Idempotent: running it twice adds nothing the second time. Local rows win on id
collisions. Output is sorted by (channel, numeric post number). Then rerun tg_calls.py.
Stdlib only; never touches the network.
"""
import argparse
import json
import re
from pathlib import Path

DEFAULT_LOCAL = Path(__file__).parent / "data" / "telegram_funnel" / "posts_archive.jsonl"


def load(path):
    rows = []
    p = Path(path)
    if not p.exists():
        return rows
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            r = json.loads(line)
        except ValueError:
            continue
        if isinstance(r, dict) and r.get("id"):
            rows.append(r)
    return rows


def sort_key(r):
    m = re.match(r"(.*?)/(\d+)$", str(r["id"]))
    return (m.group(1), int(m.group(2))) if m else (str(r["id"]), 0)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("remote")
    ap.add_argument("--local", default=str(DEFAULT_LOCAL))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    local = load(a.local)
    remote = load(a.remote)
    seen = {r["id"]: r for r in local}
    added = 0
    for r in remote:
        if r["id"] not in seen:
            seen[r["id"]] = r
            added += 1
    print(f"local {len(local)} + remote {len(remote)} -> merged {len(seen)} (added {added})")
    if a.dry_run or added == 0:
        return
    out = sorted(seen.values(), key=sort_key)
    tmp = Path(a.local).with_suffix(".jsonl.tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in out), encoding="utf-8")
    tmp.replace(a.local)


if __name__ == "__main__":
    main()
