import sys, json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))
from afterhour import profile_id, fetch_all_posts, normalize

# These are the unique usernames we extracted from the native feed swipe
usernames = [
    "883Ismygovtname", 
    "NewFishBigPond", 
    "MarketVictor", 
    "Dallaslongcall", 
    "RoyaltyTradez", 
    "PeakNate", 
    "geo21208", 
    "SonnySide", 
    "TRON"
]

following_data = {}

print("Extracting full JSON data for Following list via API...")
for u in usernames:
    try:
        pid = profile_id(u)
        api_link = f"https://api.afterhour.com/social/feed?take=50&contentTypes=post&authorId={pid}"
        print(f"\n[+] {u} ({pid})")
        print(f"    Link: {api_link}")
        
        posts = fetch_all_posts(pid)
        following_data[u] = {
            "profile_id": pid,
            "api_link": api_link,
            "posts_extracted": len(posts),
            "latest_post": normalize(posts[0]) if posts else None
        }
        print(f"    -> Extracted {len(posts)} total posts.")
    except Exception as e:
        print(f"[-] Failed to fetch {u}: {e}")

with open(str(BASE_DIR / "data" / "following" / "following_sentiment.json"), "w") as f:
    json.dump(following_data, f, indent=2)

print("\nSaved all extracted data to following_sentiment.json")
