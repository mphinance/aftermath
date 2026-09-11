import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone, timedelta

with open('/home/mpha/artemis/afterhour/data/following/@RyanLP_all_posts.json') as f:
    posts = json.load(f)

# Sort chronologically
posts_sorted = sorted(posts, key=lambda x: x.get('createdAt') or x.get('created_at') or x.get('date'))

print(f"Total posts: {len(posts_sorted)}")

# 1. Date range and temporal distribution
dates = []
dow_counter = Counter()
hour_utc_counter = Counter()
month_counter = Counter()
edt = timezone(timedelta(hours=-4))

for p in posts_sorted:
    raw_dt = p.get('createdAt') or p.get('created_at') or p.get('date')
    dt = datetime.fromisoformat(raw_dt.replace('Z', '+00:00'))
    dates.append(dt)
    dow_counter[dt.strftime('%A')] += 1
    dt_eastern = dt.astimezone(edt)
    hour_utc_counter[dt_eastern.hour] += 1
    month_counter[dt.strftime('%Y-%m')] += 1

start_date = min(dates)
end_date = max(dates)
total_days = (end_date - start_date).total_seconds() / 86400.0
total_weeks = total_days / 7.0

print(f"Start date: {start_date}")
print(f"End date: {end_date}")
print(f"Total calendar days: {total_days:.1f}")
print(f"Total weeks: {total_weeks:.2f}")
print(f"Posts/week: {len(posts_sorted) / total_weeks:.2f}")
print(f"Posts/day: {len(posts_sorted) / total_days:.2f}")

print("\n--- Day of Week Distribution ---")
days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
for d in days_order:
    cnt = dow_counter[d]
    pct = (cnt / len(posts_sorted)) * 100
    print(f"{d:10s}: {cnt:3d} ({pct:5.1f}%)")

print("\n--- Hourly Eastern Distribution (EDT UTC-4) ---")
for h in range(24):
    cnt = hour_utc_counter[h]
    pct = (cnt / len(posts_sorted)) * 100
    bar = '#' * int(cnt)
    print(f"{h:02d}:00 EDT | {cnt:2d} ({pct:4.1f}%) | {bar}")

print("\n--- Monthly Progression ---")
for m in sorted(month_counter.keys()):
    cnt = month_counter[m]
    print(f"{m}: {cnt:3d} posts")

# 2. Capital & Account Balance
amounts = []
amount_by_date = []
for p in posts_sorted:
    amt = p.get('amount_k')
    raw_dt = p.get('createdAt') or p.get('created_at') or p.get('date')
    if amt is not None:
        amounts.append(amt)
        amount_by_date.append((raw_dt[:10], amt, p.get('title')))

print("\n--- Capital Observations ---")
print(f"Min amount_k: {min(amounts)}")
print(f"Max amount_k: {max(amounts)}")

# 3. Ticker Universe
ticker_counter = Counter()
futures_counter = Counter()

false_positives = {'USD', 'CEO', 'ATH', 'DTE', 'FOMO', 'FREE', 'BEST', 'EST', 'PST', 'AM', 'PM', 'THE', 'AND', 'FOR', 'ALL', 'A', 'I', 'AI', 'RH', 'PDT', 'BPR', 'ROC', 'POP', 'IV', 'ZEBRA', 'OTM', 'ITM', 'ATM', 'CSP', 'CC', 'CCS', 'PCS', 'CDS', 'PDS', 'TONIGHT', 'LIVE', 'DISCORD', 'RECAP', 'WEEKLY', 'BUY', 'SELL', 'CALL', 'PUT', 'LEAP', 'LEAPS', 'NEW'}

futures_symbols = ['/ES', '/MES', '/NQ', '/MNQ', '/RTY', '/CL', '/ZS', '/GC', '/SI', '/ZB', '/ZN', '/ZT', '/6E', '/6B', '/6J', '/6S', '/6C', '/6A', 'SPX', 'NDX', 'RUT']

for p in posts_sorted:
    text = (p.get('title', '') + ' ' + p.get('body', '') + ' ' + str(p.get('tickers', ''))).upper()
    
    # cashtags
    cashtags = re.findall(r'\$([A-Z]{1,6})\b', text)
    for c in cashtags:
        if c not in false_positives and len(c) > 1:
            ticker_counter[c] += 1
            
    # raw tickers field
    raw_tick = str(p.get('tickers', '')).upper()
    for t in re.split(r'[,;\s]+', raw_tick):
        t = t.strip()
        if t and t not in false_positives and len(t) > 1:
            ticker_counter[t] += 1
            
    # futures & index options
    for f in futures_symbols:
        if f in text:
            futures_counter[f] += 1

print("\n--- Top Tickers ($ Cashtags & Mentioned) ---")
for t, cnt in ticker_counter.most_common(35):
    print(f"{t:10s}: {cnt:3d}")

print("\n--- Futures & Index Mentions ---")
for f, cnt in futures_counter.most_common(15):
    print(f"{f:10s}: {cnt:3d}")

# 4. Weekly Recaps Parsing
recaps = []
for idx, p in enumerate(posts_sorted):
    title = p.get('title', '')
    body = p.get('body', '')
    dt = (p.get('createdAt') or p.get('created_at') or p.get('date'))[:10]
    amt = p.get('amount_k')
    
    pl_match = re.search(r'Closed Profit/\(Loss\):\s*([-$0-9,.]+)', body)
    cum_match = re.search(r'Cumulative P/?\(?L\)?:\s*([-$0-9,.]+)', body)
    open_pos = re.search(r'Open Positions:\s*([0-9]+)', body)
    closed_trades = re.search(r'Closed Trades:\s*([0-9]+)', body)
    managed_trades = re.search(r'Managed Trades:\s*([0-9]+)', body)
    opened_trades = re.search(r'Opened Trades:\s*([0-9]+)', body)
    
    if pl_match or 'weekly recap' in title.lower():
        recaps.append({
            'post_num': idx + 1,
            'date': dt,
            'title': title,
            'amount_k': amt,
            'pnl': pl_match.group(1) if pl_match else 'N/A',
            'cum_pnl': cum_match.group(1) if cum_match else 'N/A',
            'open_pos': open_pos.group(1) if open_pos else 'N/A',
            'closed_trades': closed_trades.group(1) if closed_trades else 'N/A',
            'managed_trades': managed_trades.group(1) if managed_trades else 'N/A',
            'opened_trades': opened_trades.group(1) if opened_trades else 'N/A',
        })

print(f"\n--- Total Recaps with PnL: {len(recaps)} ---")
for r in recaps:
    print(f"Post #{r['post_num']:3d} | {r['date']} | amt_k: {str(r['amount_k']):7s} | PnL: {r['pnl']:10s} | Cum: {r['cum_pnl']:12s} | Open: {r['open_pos']:3s} | Closed: {r['closed_trades']:3s} | Title: {r['title'][:35]}")

