import json
import re

with open('/home/mpha/artemis/afterhour/data/following/@RyanLP_all_posts.json') as f:
    posts = json.load(f)

posts_sorted = sorted(posts, key=lambda x: x.get('createdAt') or x.get('created_at') or x.get('date'))

# Search for any comments or text mentioning account balance or small account
for i, p in enumerate(posts_sorted):
    b = p.get('body', '') + ' ' + p.get('title', '')
    amt = p.get('amount_k')
    dt = (p.get('createdAt') or p.get('created_at') or p.get('date'))[:10]
    
    # check for interesting keywords
    for kw in ['challenge', 'small account', 'linked', 'unlink', 'plaid', 'switch', 'deposit', 'withdraw', 'transfer', 'tasty', '1k', '1,000', '1000', 'gimmick', 'receipts']:
        if re.search(r'\b' + kw + r'\b', b, re.I):
            print(f"Post #{i+1} [{dt}] amt={amt} matched '{kw}': {p.get('title')}")
            # print match
            for line in b.split('\n'):
                if re.search(r'\b' + kw + r'\b', line, re.I):
                    print(f"    {line}")
            print("-" * 50)
            break
