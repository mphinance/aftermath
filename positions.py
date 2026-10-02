#!/usr/bin/env python3
"""
Rebuild a trader's position history from the broker-verified portfolio snapshots
attached to their posts, and diff it into opens / adds / trims / closes per underlying.

Each post's portfolioSnapshot only carries the legs for the securities tagged on that
post, so a snapshot is a complete view of *those* underlyings at that moment and says
nothing about anything else. Changes are therefore diffed per underlying, between
consecutive snapshots that include it.

Option quantities are in shares (400000 = 4,000 contracts); shorts are negative.

    python3 positions.py wTF                # fetch live
    python3 positions.py wTF --raw raw.json # reuse an unnormalized fetch_all_posts dump
"""
import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

LEG_FIELDS = (
    "tickerSymbol", "rootTickerSymbol", "securityName", "type", "optionsContractType",
    "optionsStrikePrice", "optionsExpirationDate", "quantity", "price", "value",
    "costBasis", "profit", "profitPercent",
)


def legs_from_raw(raw):
    """Flatten every snapshot leg, one row per (snapshot, leg), deduped on snapshot time."""
    seen, rows = set(), []
    for item in raw:
        post = item.get("post") or {}
        snap = item.get("portfolioSnapshot") or {}
        asof = snap.get("verifiedAsOf")
        for leg in snap.get("positionSnapshots") or []:
            if not leg.get("quantity"):
                continue  # zero-quantity legs are closed positions the broker still lists
            key = (asof, leg.get("tickerSymbol"))
            if not asof or key in seen:
                continue
            seen.add(key)
            row = {k: leg.get(k) for k in LEG_FIELDS}
            row["optionsExpirationDate"] = (row["optionsExpirationDate"] or "")[:10] or None
            row["asof"] = asof
            row["post_id"] = post.get("id") or item.get("id")
            row["post_title"] = post.get("title", "")
            row["share_url"] = post.get("shareUrl", "")
            row["account_value"] = snap.get("totalValue")
            rows.append(row)
    rows.sort(key=lambda r: (r["asof"], r["rootTickerSymbol"] or "", r["tickerSymbol"] or ""))
    return rows


def account_from_raw(raw):
    """One row per distinct snapshot: whole-account value, cash (negative = margin debit), basis, P&L."""
    seen, rows = set(), []
    for item in raw:
        snap = item.get("portfolioSnapshot") or {}
        asof = snap.get("verifiedAsOf")
        if not asof or asof in seen or snap.get("totalValue") is None:
            continue
        seen.add(asof)
        rows.append({
            "asof": asof, "total_value": snap.get("totalValue"), "cash_balance": snap.get("cashBalance"),
            "cost_basis": snap.get("costBasis"), "profit": snap.get("profit"),
            "profit_today": snap.get("profitToday"), "legs_attached": len(snap.get("positionSnapshots") or []),
            "post_id": (item.get("post") or {}).get("id") or item.get("id"),
        })
    return sorted(rows, key=lambda r: r["asof"])


def describe(leg):
    if leg["type"] != "DERIVATIVE":
        return f"{leg['tickerSymbol']} shares"
    strike = leg["optionsStrikePrice"]
    strike = f"{strike:g}" if isinstance(strike, (int, float)) else strike
    return f"{leg['rootTickerSymbol']} ${strike} {leg['optionsContractType']} {leg['optionsExpirationDate']}"


def units(leg, qty):
    """Human quantity: contracts for options, shares for equity; sign kept."""
    if leg["type"] == "DERIVATIVE":
        return f"{qty / 100:+,.0f} ct"
    return f"{qty:+,.0f} sh"


def diff_changes(rows):
    """Per underlying, compare each snapshot's book to the previous one that included it."""
    by_root = defaultdict(lambda: defaultdict(dict))
    for r in rows:
        by_root[r["rootTickerSymbol"]][r["asof"]][r["tickerSymbol"]] = r

    changes = []
    for root, snaps in by_root.items():
        prev = {}
        for asof in sorted(snaps):
            book = snaps[asof]
            for sym in sorted(set(prev) | set(book)):
                old, new = prev.get(sym), book.get(sym)
                q0 = old["quantity"] if old else 0
                q1 = new["quantity"] if new else 0
                if q0 == q1:
                    continue
                leg = new or old
                if not old:
                    action = "OPEN SHORT" if q1 < 0 else "OPEN LONG"
                elif not new:
                    expired = leg["optionsExpirationDate"] and leg["optionsExpirationDate"] < asof[:10]
                    action = "EXPIRED/GONE" if expired else "CLOSED"
                elif (q0 > 0) != (q1 > 0):
                    action = "FLIP"
                elif abs(q1) > abs(q0):
                    action = "ADD"
                else:
                    action = "TRIM"
                changes.append({
                    "asof": asof, "root": root, "leg": describe(leg), "action": action,
                    "qty_before": q0, "qty_after": q1,
                    "delta": units(leg, q1 - q0), "position": units(leg, q1) if new else "flat",
                    "price": new["price"] if new else old["price"],
                    "value_after": new["value"] if new else 0,
                    "unrealized_profit": new["profit"] if new else None,
                    "last_seen_profit": old["profit"] if old and not new else None,
                    "share_url": next(iter(book.values()))["share_url"],
                })
            prev = book
    changes.sort(key=lambda c: (c["asof"], c["root"], c["leg"]))
    return changes


def money(x):
    return "—" if x is None else f"${x/1e6:,.2f}M" if abs(x) >= 1e6 else f"${x:,.0f}"


def write_report(username, rows, changes, path):
    roots = defaultdict(list)
    for c in changes:
        roots[c["root"]].append(c)
    legs_per_root = defaultdict(int)
    for r in rows:
        legs_per_root[r["rootTickerSymbol"]] += 1
    order = sorted(roots, key=lambda k: -legs_per_root[k])

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# Position Change Log: @{username}\n\n")
        f.write("Built from the broker-verified `portfolioSnapshot` attached to each post "
                f"({len({r['asof'] for r in rows})} snapshots, {len(rows)} position legs). "
                "A snapshot only shows the underlyings tagged on that post, so each change below "
                "is measured against the previous snapshot that included the same underlying — "
                "the trade happened somewhere between those two timestamps. "
                "Option sizes are contracts; negative = short, so `ADD` on a short means the short got bigger. `EXPIRED/GONE` means the leg vanished "
                "after its expiry date; `CLOSED` means it vanished before expiry.\n\n")
        f.write("| Underlying | Legs seen | Changes |\n|---|---:|---:|\n")
        for root in order:
            f.write(f"| {root} | {legs_per_root[root]} | {len(roots[root])} |\n")
        for root in order:
            f.write(f"\n## ${root}\n\n")
            f.write("| Snapshot (UTC) | Leg | Action | Change | Position after | Price | Value after | Unrealized P&L |\n")
            f.write("|---|---|---|---:|---:|---:|---:|---:|\n")
            for c in roots[root]:
                pnl = c["unrealized_profit"] if c["unrealized_profit"] is not None else c["last_seen_profit"]
                note = " (last seen)" if c["unrealized_profit"] is None and pnl is not None else ""
                f.write(f"| {c['asof'][:16].replace('T', ' ')} | {c['leg']} | {c['action']} | {c['delta']} | "
                        f"{c['position']} | {c['price']:g} | {money(c['value_after'])} | {money(pnl)}{note} |\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("username")
    ap.add_argument("--raw", help="unnormalized fetch_all_posts JSON dump")
    args = ap.parse_args()
    username = args.username.lstrip("@")

    if args.raw:
        raw = json.load(open(args.raw, encoding="utf-8"))
    else:
        from afterhour import fetch_all_posts, profile_id
        raw = fetch_all_posts(profile_id(username))

    rows = legs_from_raw(raw)
    changes = diff_changes(rows)

    out_dir = BASE_DIR / "data" / "positions"
    rep_dir = BASE_DIR / "reports" / "positions"
    out_dir.mkdir(parents=True, exist_ok=True)
    rep_dir.mkdir(parents=True, exist_ok=True)
    json.dump({"account": account_from_raw(raw), "legs": rows, "changes": changes}, open(out_dir / f"@{username}_positions.json", "w"), indent=1)
    write_report(username, rows, changes, rep_dir / f"@{username}_position_changes.md")
    print(f"{len(rows)} legs, {len(changes)} changes -> data/positions/@{username}_positions.json, "
          f"reports/positions/@{username}_position_changes.md")


if __name__ == "__main__":
    main()
