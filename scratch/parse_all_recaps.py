import json
import re

with open('/home/mpha/artemis/afterhour/data/following/@RyanLP_all_posts.json') as f:
    posts = json.load(f)

posts_sorted = sorted(posts, key=lambda x: x.get('createdAt') or x.get('created_at') or x.get('date'))

recap_data = []
total_closed_pnl = 0.0

for idx, p in enumerate(posts_sorted):
    title = p.get('title', '')
    body = p.get('body', '')
    dt = (p.get('createdAt') or p.get('created_at') or p.get('date'))[:10]
    amt = p.get('amount_k')
    
    # Check if recap
    if 'weekly recap' in title.lower() or 'my weekly recap' in title.lower() or 'summary' in body.lower() or 'cumulative p/' in body.lower():
        # parse closed pnl
        pl_str = None
        # look for Closed Profit/(Loss): ...
        m_pl = re.search(r'Closed Profit/\(Loss\):\s*([-$()0-9,.]+)', body)
        if m_pl:
            pl_str = m_pl.group(1).strip()
            
        m_cum = re.search(r'Cumulative P/?\(?L\)?:\s*([-$()0-9,.]+)', body)
        cum_str = m_cum.group(1).strip() if m_cum else None
        
        m_open_t = re.search(r'Opened Trades:\s*([0-9]+)', body)
        m_man_t = re.search(r'Managed Trades:\s*([0-9]+)', body)
        m_cls_t = re.search(r'Closed Trades:\s*([0-9]+)', body)
        m_opn_p = re.search(r'Open Positions:\s*([0-9]+)', body)
        
        # numeric pnl
        num_pl = None
        if pl_str:
            clean = pl_str.replace('$', '').replace(',', '')
            if clean.startswith('(') and clean.endswith(')'):
                clean = '-' + clean[1:-1]
            try:
                num_pl = float(clean)
                total_closed_pnl += num_pl
            except:
                pass
                
        recap_data.append({
            'post_num': idx + 1,
            'date': dt,
            'title': title,
            'amount_k': amt,
            'pnl_raw': pl_str,
            'pnl_num': num_pl,
            'cum_raw': cum_str,
            'opened': int(m_open_t.group(1)) if m_open_t else 0,
            'managed': int(m_man_t.group(1)) if m_man_t else 0,
            'closed': int(m_cls_t.group(1)) if m_cls_t else 0,
            'open_pos': int(m_opn_p.group(1)) if m_opn_p else 0,
            'body': body
        })

print(f"Total recaps identified: {len(recap_data)}")
print(f"Running sum of closed PnL across recaps: ${total_closed_pnl:,.2f}")
print("\nDetailed Recaps Table:")
print(f"{'Post#':5s} | {'Date':10s} | {'Amt(k)':7s} | {'Weekly PnL':12s} | {'Cum PnL':14s} | {'Opn':3s} | {'Mng':3s} | {'Cls':3s} | {'Positions':9s} | Title")
print("-" * 95)
for r in recap_data:
    pnl_display = f"${r['pnl_num']:,.2f}" if r['pnl_num'] is not None else "N/A"
    cum_display = r['cum_raw'] if r['cum_raw'] else "-"
    amt_disp = f"${r['amount_k']:.2f}k" if r['amount_k'] is not None else "N/A"
    print(f"{r['post_num']:5d} | {r['date']:10s} | {amt_disp:7s} | {pnl_display:12s} | {cum_display:14s} | {r['opened']:3d} | {r['managed']:3d} | {r['closed']:3d} | {r['open_pos']:9d} | {r['title'][:30]}")

