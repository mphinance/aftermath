import json
import logging
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

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
        for p in data.get("positionSnapshots", []):
            sid = p.get("securityId")
            ticker = sec_id_to_ticker.get(sid, sid)
            positions.append({
                "ticker": ticker,
                "quantity": p.get("quantity", 0),
                "value": p.get("value", 0),
                "cost_basis": p.get("costBasis", 0),
                "profit": p.get("profit", 0),
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
    top_syms = ", ".join([p["ticker"] for p in w["top_positions"][:3] if p["ticker"]])
    followers = w["followers"]
    ratio = f"${w['total_value'] / max(1, followers):,.0f}/sub"
    print(f"#{idx:<4} @{w['username']:<19} ${w['total_value']:>14,.2f}  {followers:>8d}    {top_syms:<33} {ratio:<15}")
print("=" * 100)
