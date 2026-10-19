import gzip, json
from datetime import datetime, timezone

import ah_daily_export as D
import ah_positioning_export as P


def test_positioning_floor_and_fields(tmp_path):
    rows = [{"ticker": "NVDA", "owners": 5, "value": 9.5, "rank": 1, "chat_members": 7, "chg_pct": 1.4,
             "id": "secret", "mcap": 1},
            {"ticker": "TINY", "owners": 2, "value": 1, "rank": 2},
            {"ticker": "NULL", "owners": None}]
    with gzip.open(tmp_path / "2026-10-19.json.gz", "wb") as f:
        f.write(json.dumps({"rows": rows}).encode())
    (tmp_path / "2026-10-18.json.gz").write_bytes(b"corrupt")
    out = P.build(tmp_path, datetime(2026, 10, 19, tzinfo=timezone.utc))
    assert out["days"] == {"2026-10-19": {"NVDA": {"owners": 5, "total_value": 9.5, "rank": 1,
                                                    "chatroom_members": 7, "change_pct": 1.4}}}


def _post(i, author, tk="NVDA", day="2026-10-10"):
    return {"id": i, "ts": f"{day}T15:00:00Z", "author": author, "tickers": [tk], "stance": "bull", "sig": f"s{i}"}


def test_daily_export_author_floor():
    now = datetime(2026, 10, 19, tzinfo=timezone.utc)
    posts = [_post(1, "a"), _post(2, "b"), _post(3, "c"), _post(4, "a", "AMD"), _post(5, "b", "AMD")]
    out = D.export(posts, now)["daily"]
    assert out["NVDA"][0]["posts"] == 3 and "AMD" not in out
    assert "author" not in json.dumps(out)
