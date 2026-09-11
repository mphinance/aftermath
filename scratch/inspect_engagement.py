import json

with open('/home/mpha/artemis/afterhour/data/following/@RyanLP_all_posts.json') as f:
    posts = json.load(f)

# Sort by view count, reaction count, comment count
by_views = sorted(posts, key=lambda x: x.get('view_count') or 0, reverse=True)
by_reactions = sorted(posts, key=lambda x: x.get('reaction_count') or 0, reverse=True)
by_comments = sorted(posts, key=lambda x: x.get('comment_count') or 0, reverse=True)

print("--- TOP 10 BY VIEW COUNT ---")
for p in by_views[:10]:
    print(f"Views: {p.get('view_count'):5d} | Reacts: {p.get('reaction_count'):3d} | Comments: {p.get('comment_count'):3d} | Date: {p.get('date')} | Title: {p.get('title')}")

print("\n--- TOP 10 BY REACTION COUNT ---")
for p in by_reactions[:10]:
    print(f"Reacts: {p.get('reaction_count'):3d} | Views: {p.get('view_count'):5d} | Comments: {p.get('comment_count'):3d} | Date: {p.get('date')} | Title: {p.get('title')}")

print("\n--- TOP 10 BY COMMENT COUNT ---")
for p in by_comments[:10]:
    print(f"Comments: {p.get('comment_count'):3d} | Views: {p.get('view_count'):5d} | Reacts: {p.get('reaction_count'):3d} | Date: {p.get('date')} | Title: {p.get('title')}")

