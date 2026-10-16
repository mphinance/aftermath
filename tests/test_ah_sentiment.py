import os, sys
from datetime import datetime, timezone
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import ah_sentiment as S

NOW = datetime(2026, 10, 16, 18, 0, tzinfo=timezone.utc)


def item(pid, title, user="u1", followers=50, secs=("SPY",), ts="2026-10-16T17:00:00.000Z", topic=None):
    return {"id": "sct_" + pid, "primaryTopicKey": topic, "commentCount": 0, "createdAt": ts,
            "securities": [{"tickerSymbol": s} for s in secs],
            "post": {"id": pid, "title": title, "createdAt": ts, "viewCount": 10,
                     "shareUrl": f"https://afterhour.com/{user}/ab12/slug", "positionSnapshots": []},
            "author": {"username": user, "numFollowers": followers}}


def test_classify_open_close_and_hindsight():
    assert S.classify("Opened 10 $SPXW 7710P 10/16 @ $8.00")["stance"] == "bear"
    assert S.classify("$SPY 765 CALL 0DTE @ 1.02")["stance"] == "bull"
    c = S.classify("Closed 10 $SPX 7710P 10/16@$8.50 (Entry: $8.00) |Gain: +6.3%")
    assert c["action"] == "close" and c["stance"] == "neutral"
    assert S.classify("should've bought SPY calls")["stance"] == "neutral"
    assert S.classify("$NVDA to the moon")["basis"] == "no_contract"
    assert S.classify("watching SPY puts for tomorrow")["stance"] == "neutral"


def test_parse_item_alias_and_hash():
    p = S.parse_item(item("p1", "Opened 1 $SPXW 7700P @ 2", secs=("SPXW",)))
    assert p["tickers"] == ["SPX"] and p["hash"] == "ab12" and p["stance"] == "bear"
    assert S.parse_item({"post": {}}) is None


def test_one_vote_per_author_and_copy_paste_collapse():
    posts = [S.parse_item(item(f"a{i}", "Opened 1 $SPY 765C @ 1.00", user="same")) for i in range(5)]
    agg = S.aggregate(posts, NOW, 24)["SPY"]
    assert agg["bull"] == 1 and agg["n_voting_authors"] == 1 and agg["confidence"] == "low"
    spam = [S.parse_item(item(f"s{i}", "HIGH CONFIDENCE $FIZZ 40 CALL @ .25", user=f"bot{i}", followers=3, secs=("FIZZ",)))
            for i in range(4)]
    f = S.aggregate(spam, NOW, 24)["FIZZ"]
    assert f["bull"] == 1 and f["flags"]["duplicate_text_posts"] == 4 and f["flags"]["low_follower_author_share"] == 1.0


def test_window_excludes_old_and_net_score():
    posts = [S.parse_item(item("n1", "Opened $SPY 765C @1", user="a")),
             S.parse_item(item("n2", "Opened $SPY 760P @1", user="b")),
             S.parse_item(item("n3", "Opened $SPY 770C @1", user="c")),
             S.parse_item(item("old", "Opened $SPY 700P @1", user="d", ts="2026-10-10T17:00:00.000Z"))]
    a = S.aggregate(posts, NOW, 24)["SPY"]
    assert (a["bull"], a["bear"], a["net_score"]) == (2, 1, 0.333)
    assert a["calls_opened"] == 2 and a["puts_opened"] == 1


def test_buzz_z_requires_depth():
    posts = [S.parse_item(item("b1", "x $AAA", secs=("AAA",)))]
    assert S.buzz(posts, NOW, 24)["tickers"]["AAA"]["z"] is None
