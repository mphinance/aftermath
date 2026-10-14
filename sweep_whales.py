import json
import logging
import re
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

OCC_REGEX = re.compile(r"^([A-Z]{1,6})\s*(\d{2})(\d{2})(\d{2})([CP])(\d{8})$")

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "leaderboard"

# Load securities leaderboard
with open(DATA_DIR / "stock_leaderboard.json", encoding="utf-8") as f:
    board_data = json.load(f)

# Map security IDs to tickers
sec_id_to_ticker = {}
for s in board_data.get("securities", []):
    sec = s.get("security", {}).get("security", {})
    sid = sec.get("id")
    ticker = sec.get("tickerSymbol")
    if sid and ticker:
        sec_id_to_ticker[sid] = ticker

# Collect unique public connected users
users = {}
for s in board_data.get("securities", []):
    sec = s.get("security", {})
    for u in sec.get("ownersSample", []):
        uid = u.get("id")
        uname = u.get("username")
        if uid and uname and uname not in users and u.get("hasConnectedItems") and u.get("financialDataPrivacyMode") == "PUBLIC":
            users[uname] = u

logging.info(f"Loaded {len(users)} unique public connected users from stock_leaderboard.json")

def fetch_user_portfolio(u):
    uid = u["id"]
    url = f"https://api.afterhour.com/stonks/public/portfolio/{uid}/summary/live"
    req = urllib.request.Request(url, headers={"User-Agent": "okhttp/4.12.0"})
    try:
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        val = data.get("totalValue") or data.get("value") or 0.0
        pnl = data.get("profit") or 0.0
        pnl_pct = data.get("profitPercent") or 0.0
        pnl_today = data.get("profitToday") or 0.0
        cost_basis = data.get("costBasis") or 0.0
        cash = data.get("cashBalance") or 0.0

        positions = []
        options_count = 0
        options_val = 0.0
        equity_val = 0.0

        for p in data.get("positionSnapshots", []):
            sid = p.get("securityId")
            raw_ticker = (p.get("tickerSymbol") or sec_id_to_ticker.get(sid) or p.get("rootTickerSymbol") or sid or "").strip()
            root_ticker = (p.get("rootTickerSymbol") or "").strip()
            sec_name = (p.get("securityName") or raw_ticker).strip()
            raw_type = (p.get("type") or "EQUITY").upper()

            qty = float(p.get("quantity", 0) or 0)
            pos_val = round(float(p.get("value", 0) or 0), 2)
            cost_b = round(float(p.get("costBasis", 0) or 0), 2)
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
                shares_per_contract = int(p.get("optionsSharesPerContract") or 100)
                contracts = round(qty / shares_per_contract) if shares_per_contract else round(qty / 100)

                if p.get("optionsContractType"):
                    opt_type = str(p.get("optionsContractType")).upper()
                if p.get("optionsStrikePrice") is not None:
                    strike = float(p.get("optionsStrikePrice"))
                if p.get("optionsExpirationDate"):
                    expiry = str(p.get("optionsExpirationDate"))[:10]
                if not root_ticker and p.get("rootTickerSymbol"):
                    root_ticker = p.get("rootTickerSymbol").strip()

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

                options_count += 1
                options_val += pos_val
            else:
                root_ticker = root_ticker or raw_ticker
                clean_symbol = root_ticker
                if raw_type == "ETF":
                    asset_type = "ETF"
                elif raw_type == "CRYPTO":
                    asset_type = "CRYPTO"
                else:
                    asset_type = "STOCK"
                equity_val += pos_val

            positions.append({
                "ticker": raw_ticker,
                "root_ticker": root_ticker,
                "clean_symbol": clean_symbol,
                "name": sec_name,
                "security_id": sid,
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
                "value": pos_val,
                "cost_basis": cost_b,
                "profit": prof,
                "profit_today": prof_today,
                "profit_percent": prof_pct,
            })
        
        # Sort positions by value descending
        positions.sort(key=lambda p: p["value"], reverse=True)

        return {
            "username": u.get("username"),
            "profile_id": uid,
            "followers": u.get("numFollowers", 0),
            "following": u.get("numFollowing", 0),
            "total_likes": u.get("numTotalLikes", 0),
            "total_value": round(val, 2),
            "cost_basis": round(cost_basis, 2),
            "profit": round(pnl, 2),
            "profit_percent": round(pnl_pct, 2),
            "profit_today": round(pnl_today, 2),
            "cash_balance": round(cash, 2),
            "verified_as_of": data.get("verifiedAsOf"),
            "positions_count": len(positions),
            "options_count": options_count,
            "options_value": round(options_val, 2),
            "equity_value": round(equity_val, 2),
            "options_percent": round((options_val / max(1, val)) * 100, 1),
            "top_positions": positions[:5],
            "all_positions": positions,
        }
    except Exception as e:
        return {"username": u.get("username"), "profile_id": uid, "error": str(e)}

# Sweep all users with ThreadPoolExecutor
logging.info(f"Starting sweep of {len(users)} users with 8 worker threads...")
t0 = time.time()
with ThreadPoolExecutor(max_workers=8) as pool:
    results = list(pool.map(fetch_user_portfolio, list(users.values())))

elapsed = time.time() - t0
logging.info(f"Completed sweep in {elapsed:.2f} seconds")

# Filter successful
successful = [r for r in results if "error" not in r and r.get("total_value", 0) > 0]
successful.sort(key=lambda x: x["total_value"], reverse=True)

logging.info(f"Found {len(successful)} active verified portfolios with positive balance")

# Save complete ranked whale list
out_file = DATA_DIR / "all_verified_whales_ranked.json"
with open(out_file, "w", encoding="utf-8") as f:
    json.dump({
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_scanned": len(users),
        "total_active": len(successful),
        "whales": successful
    }, f, indent=2)

logging.info(f"[+] Saved ranked whale leaderboard to {out_file.name}")

# Print Top 20 for preview
print("\n" + "=" * 100)
print(f"{'RANK':<5} {'HANDLE':<20} {'NET WORTH ($)':<18} {'FOLLOWERS':<12} {'TOP ASSETS':<35} {'RATIO ($/FLW)':<15}")
print("=" * 100)
for idx, w in enumerate(successful[:25], 1):
    top_syms = ", ".join([p.get("clean_symbol") or p["ticker"] for p in w["top_positions"][:3] if p.get("ticker")])
    followers = w["followers"]
    ratio = f"${w['total_value'] / max(1, followers):,.0f}/sub"
    print(f"#{idx:<4} @{w['username']:<19} ${w['total_value']:>14,.2f}  {followers:>8d}    {top_syms:<33} {ratio:<15}")
print("=" * 100)
