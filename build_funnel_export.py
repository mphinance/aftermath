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
        "intrinsic", "worthless", "pnl_per_contract", "return_pct", "win",
        "path_category", "path_fill", "path_mfe_pct", "path_mae_pct", "path_end_ret_pct", "path_volume", "path_tp50_sl50",
        "path_tp50_sl50_ret", "path_quoted_vs_fill_pct", "text"]
PATH_KEYS = ["category", "fill", "mfe_pct", "mae_pct", "end_ret_pct", "volume", "tp50_sl50", "tp50_sl50_ret", "quoted_vs_fill_pct"]


def path_key(c):
    """A post id can carry several contracts, so the join also needs the contract itself."""
    return (c.get("id"), c.get("ticker"), c.get("side"), c.get("strike"), c.get("expiry"))


def main():
    tf = BASE / "data" / "telegram_funnel"
    calls = [c for c in read_jsonl(tf / "calls.jsonl") if is_public(c.get("channel"))]
    by_id = {}
    for o in read_jsonl(tf / "outcomes.jsonl"):
        for i in o.get("ids") or []:
            by_id[i] = o
    paths = {}
    for p in read_jsonl(tf / "option_paths.jsonl"):       # local only (built from Alpaca bars); absent on the server
        if p.get("status") == "scored" and p.get("id"):
            paths[path_key(p)] = {k: p[k] for k in PATH_KEYS if k in p}
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
        if c.get("action") == "open" and path_key(c) in paths:
            r["path"] = paths[path_key(c)]
        rows.append(r)
    scored = [r for r in rows if (r.get("outcome") or {}).get("status") == "scored"]
    posted = [r["posted"][:10] for r in rows if r.get("posted")]
    out = {"generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), "credit": SITE, "disclaimer": DISCLAIMER,
           "quoted_results_are_channel_claims": CLAIMS_NOTE,
           "path_note": "'path' is present on scored option opens when the export is built where the local 5-minute bar archive exists: the contract's own traded price after the post (fill = open of the first 5-minute bar at or after the post; intraday calls get 30 minutes, daily callouts the next regular session). Bars are trade prints, no spread or slippage. Method: https://ah.mphinance.com/scorecard",
           "note": "Every parsed callout from public Telegram channels (repeat posts included, flagged echo=true). 'outcome' is "
                   "present when the callout is a scored option open: hold-to-expiry intrinsic against the entry the channel quoted, "
                   "no slippage or fees. Parsing is automatic and can be wrong; the original text is included.",
           "count": len(rows), "scored_count": len(scored), "path_count": sum(1 for r in rows if "path" in r),
           "window_start": min(posted) if posted else None, "window_end": max(posted) if posted else None,
           "calls": rows}
    API.mkdir(exist_ok=True)
    (API / "funnel-calls-full.json").write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
    with (API / "funnel-calls-full.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(COLS)
        for r in rows:
            o = r.get("outcome") or {}
            pa = r.get("path") or {}
            w.writerow([r.get("id"), r.get("channel"), r.get("posted"), r.get("ticker"), r.get("kind"), r.get("side"),
                        r.get("strike"), r.get("expiry"), r.get("entry_price"), r.get("exit_price"), r.get("action"),
                        r.get("result_pct"), int(r["echo"]), ";".join(r["parse_flags"]), r.get("open_id"), o.get("status"),
                        o.get("reason"), o.get("expiry_effective"), o.get("underlying_close_at_expiry"), o.get("intrinsic"),
                        o.get("worthless"), o.get("pnl_per_contract"), o.get("return_pct"), o.get("win"),
                        *[pa.get(k) for k in PATH_KEYS],
                        (r.get("text") or "").replace("\n", " / ")])
    print(f"api/funnel-calls-full.json + .csv: {len(rows)} callouts ({len(scored)} scored, {out['path_count']} with price paths), {out['window_start']} to {out['window_end']}")


if __name__ == "__main__":
    main()
