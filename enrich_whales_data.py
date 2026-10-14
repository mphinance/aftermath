#!/usr/bin/env python3
"""
Enrich existing all_verified_whales_ranked.json with full options metadata,
OCC symbol decoding, contracts math, and whale-level options exposure metrics.
"""
import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "leaderboard" / "all_verified_whales_ranked.json"

OCC_REGEX = re.compile(r"^([A-Z]{1,6})\s*(\d{2})(\d{2})(\d{2})([CP])(\d{8})$")

def parse_position_dict(p):
    raw_ticker = (p.get("ticker") or p.get("tickerSymbol") or "").strip()
    root_ticker = (p.get("root_ticker") or p.get("rootTickerSymbol") or "").strip()
    sec_name = (p.get("name") or p.get("securityName") or raw_ticker).strip()
    raw_type = (p.get("type") or "EQUITY").upper()
    
    qty = float(p.get("quantity", 0) or 0)
    val = round(float(p.get("value", 0) or 0), 2)
    cost = round(float(p.get("cost_basis", p.get("costBasis", 0)) or 0), 2)
    prof = round(float(p.get("profit", 0) or 0), 2)
    price = round(float(p["price"]), 2) if p.get("price") is not None else None
    prof_today = round(float(p["profitToday"]), 2) if p.get("profitToday") is not None else round(float(p.get("profit_today", 0) or 0), 2)
    prof_pct = round(float(p["profitPercent"]), 2) if p.get("profitPercent") is not None else round(float(p.get("profit_percent", 0) or 0), 2)

    m = OCC_REGEX.match(raw_ticker)
    is_derivative = (raw_type == "DERIVATIVE") or bool(p.get("optionsContractType")) or bool(m)

    opt_type = None
    strike = None
    expiry = None
    contracts = None
    shares_per_contract = 100

    if is_derivative:
        shares_per_contract = int(p.get("optionsSharesPerContract") or p.get("shares_per_contract") or 100)
        contracts = round(qty / shares_per_contract) if shares_per_contract else round(qty / 100)

        # 1. Check API fields if present
        if p.get("optionsContractType"):
            opt_type = str(p.get("optionsContractType")).upper()
        if p.get("optionsStrikePrice") is not None:
            strike = float(p.get("optionsStrikePrice"))
        if p.get("optionsExpirationDate"):
            expiry = str(p.get("optionsExpirationDate"))[:10]
        if not root_ticker and p.get("rootTickerSymbol"):
            root_ticker = p.get("rootTickerSymbol").strip()

        # 2. OCC regex decoding
        if m:
            if not root_ticker:
                root_ticker = m.group(1).strip()
            if not expiry:
                expiry = f"20{m.group(2)}-{m.group(3)}-{m.group(4)}"
            if not opt_type:
                opt_type = "CALL" if m.group(5) == "C" else "PUT"
            if strike is None:
                strike = int(m.group(6)) / 1000.0

        if not root_ticker:
            root_ticker = raw_ticker

        strike_str = f"{strike:g}" if isinstance(strike, (int, float)) else str(strike or "")
        clean_symbol = f"{root_ticker} ${strike_str}{opt_type[0] if opt_type else ''} {expiry or ''}".strip()
        asset_type = f"OPTION_{opt_type}" if opt_type else "OPTION"
    else:
        root_ticker = root_ticker or raw_ticker
        clean_symbol = root_ticker
        if raw_type == "ETF":
            asset_type = "ETF"
        elif raw_type == "CRYPTO":
            asset_type = "CRYPTO"
        else:
            asset_type = "STOCK"

    return {
        "ticker": raw_ticker,
        "root_ticker": root_ticker,
        "clean_symbol": clean_symbol,
        "name": sec_name,
        "security_id": p.get("security_id") or p.get("securityId"),
        "type": "DERIVATIVE" if is_derivative else raw_type,
        "asset_type": asset_type,
        "is_option": is_derivative,
        "option_type": opt_type,
        "strike": strike,
        "expiry": expiry,
        "contracts": contracts,
        "shares_per_contract": shares_per_contract,
        "quantity": qty,
        "price": price,
        "value": val,
        "cost_basis": cost,
        "profit": prof,
        "profit_today": prof_today,
        "profit_percent": prof_pct,
    }


def enrich_whales_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    whales = data.get("whales", [])
    total_opt_count = 0
    total_opt_val = 0.0

    for w in whales:
        enriched_positions = []
        w_opt_cnt = 0
        w_opt_val = 0.0
        w_eq_val = 0.0

        for p in w.get("all_positions", []):
            ep = parse_position_dict(p)
            enriched_positions.append(ep)
            if ep["is_option"]:
                w_opt_cnt += 1
                w_opt_val += ep["value"]
                total_opt_count += 1
                total_opt_val += ep["value"]
            else:
                w_eq_val += ep["value"]

        enriched_positions.sort(key=lambda x: x["value"], reverse=True)
        w["all_positions"] = enriched_positions
        w["top_positions"] = enriched_positions[:5]
        w["positions_count"] = len(enriched_positions)
        w["options_count"] = w_opt_cnt
        w["options_value"] = round(w_opt_val, 2)
        w["equity_value"] = round(w_eq_val, 2)
        w["options_percent"] = round((w_opt_val / max(1, w.get("total_value", 1))) * 100, 1)

    data["total_options_count"] = total_opt_count
    data["total_options_value"] = round(total_opt_val, 2)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"Successfully enriched {len(whales)} whales with options metadata.")
    print(f"Total options detected: {total_opt_count} (${total_opt_val:,.2f} total market value).")


if __name__ == "__main__":
    enrich_whales_data()
