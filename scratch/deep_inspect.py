import json

with open('/home/mpha/artemis/afterhour/data/following/@RyanLP_all_posts.json') as f:
    posts = json.load(f)

posts_sorted = sorted(posts, key=lambda x: x.get('createdAt') or x.get('created_at') or x.get('date'))

# Let's inspect posts where amount_k changed dramatically:
# Post 1-8: 1M
# Post 9: 0
# Post 58: 55.5k
# Post 160 -> 161: 32k -> 9.19k
# Post 164 -> 165: 8.7k -> 5.1k -> 3.0k
# Post 167 -> 168: 3.0k -> 22.0k
# Post 175 -> 176: 16.9k -> 0.97k

indices_to_check = [0, 1, 7, 8, 9, 56, 57, 58, 125, 159, 160, 161, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 186, 187, 188, 190, 191, 192]

for i in indices_to_check:
    if i < len(posts_sorted):
        p = posts_sorted[i]
        dt = (p.get('createdAt') or p.get('created_at') or p.get('date'))[:10]
        print(f"=== POST #{i+1} [{dt}] amt_k={p.get('amount_k')} | Title: {p.get('title')} ===")
        print(p.get('body'))
        print("-" * 60)

