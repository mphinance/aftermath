#!/usr/bin/env python3
"""Build the FULL parsed-callout export: api/funnel-calls-full.json and api/funnel-calls-full.csv.

Unlike api/funnel-calls.json (newest 1,000, for the /signals page) this holds every parsed callout from public
Telegram channels back to the start of the archive, each joined to its scored outcome where one exists. Repeat
posts are included and flagged (parse_flags, echo=true) so consumers can filter. Inputs: data/telegram_funnel/
calls.jsonl and outcomes.jsonl. Run standalone or from scripts/run_watch.sh."""
import csv, json
from datetime import datetime, timezone
from pathlib import Path
from build_funnel_calls import read_jsonl, is_public, OUTCOME_KEYS, SITE, DISCLAIMER, CLAIMS_NOTE

BASE = Path(__file__).resolve().parent
API = BASE / "api"
TEXT_LEN = 600
COLS = ["id", "channel", "posted", "ticker", "kind", "side", "strike", "expiry", "entry_price", "exit_price", "action",
        "result_pct", "echo", "parse_flags", "open_id", "status", "reason", "expiry_effective", "underlying_close_at_expiry",
        "intrinsic", "worthless", "pnl_per_contract", "return_pct", "win", "text"]


def main():
    tf = BASE / "data" / "telegram_funnel"
    calls = [c for c in read_jsonl(tf / "calls.jsonl") if is_public(c.get("channel"))]
    by_id = {}
    for o in read_jsonl(tf / "outcomes.jsonl"):
        for i in o.get("ids") or []:
            by_id[i] = o
    calls.sort(key=lambda c: (c.get("posted") or "", c.get("id") or ""))
    rows = []
    for c in calls:
        flags = c.get("parse_flags") or []
        r = {k: c.get(k) for k in ("id", "channel", "posted", "ticker", "kind", "side", "strike", "expiry", "entry_price",
                                   "exit_price", "action", "result_pct", "open_id")}
        r["echo"] = bool({"duplicate_echo", "cross_channel_echo"} & set(flags))
        r["parse_flags"] = flags
        t = (c.get("text") or "").strip()
        r["text"] = t if len(t) <= TEXT_LEN else t[:TEXT_LEN - 1].rstrip() + "..."
        o = by_id.get(c.get("id"))
        if o:
            r["outcome"] = {k: o[k] for k in OUTCOME_KEYS if k in o}
        rows.append(r)
    scored = [r for r in rows if (r.get("outcome") or {}).get("status") == "scored"]
    posted = [r["posted"][:10] for r in rows if r.get("posted")]
    out = {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "credit": SITE, "disclaimer": DISCLAIMER,
           "quoted_results_are_channel_claims": CLAIMS_NOTE,
           "note": "Every parsed callout from public Telegram channels (repeat posts included, flagged echo=true). 'outcome' is "
                   "present when the callout is a scored option open: hold-to-expiry intrinsic against the entry the channel quoted, "
                   "no slippage or fees. Parsing is automatic and can be wrong; the original text is included.",
           "count": len(rows), "scored_count": len(scored),
           "window_start": min(posted) if posted else None, "window_end": max(posted) if posted else None,
           "calls": rows}
    API.mkdir(exist_ok=True)
    (API / "funnel-calls-full.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    with (API / "funnel-calls-full.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(COLS)
        for r in rows:
            o = r.get("outcome") or {}
            w.writerow([r.get("id"), r.get("channel"), r.get("posted"), r.get("ticker"), r.get("kind"), r.get("side"),
                        r.get("strike"), r.get("expiry"), r.get("entry_price"), r.get("exit_price"), r.get("action"),
                        r.get("result_pct"), int(r["echo"]), ";".join(r["parse_flags"]), r.get("open_id"), o.get("status"),
                        o.get("reason"), o.get("expiry_effective"), o.get("underlying_close_at_expiry"), o.get("intrinsic"),
                        o.get("worthless"), o.get("pnl_per_contract"), o.get("return_pct"), o.get("win"),
                        (r.get("text") or "").replace("\n", " / ")])
    print(f"api/funnel-calls-full.json + .csv: {len(rows)} callouts ({len(scored)} scored), {out['window_start']} to {out['window_end']}")


if __name__ == "__main__":
    main()
