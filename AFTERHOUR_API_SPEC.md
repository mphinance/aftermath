# AfterHour API Specification & Reverse-Engineered Reference

> Complete documentation of the public, semi-public, and internal endpoints powering the [AfterHour](https://afterhour.com) mobile app (React Native / Android) and web frontend.
> Reverse-engineered from `com.afterhour` v1.x Android APK bundle and live NestJS / Cloudflare API gateway analysis.

---

## 🌐 Overview & Connection Architecture

- **Primary API Base URL**: `https://api.afterhour.com`
- **Web Frontend / Profile Resolution**: `https://afterhour.com`
- **Real-Time Chat Gateway**: `https://chatapi.afterhour.chat`
- **Static Assets / CDN**: `https://d21mnq29ucedqg.cloudfront.net`
- **Authentication**: **None required** for read-only public endpoints (stock leaderboards, ticker metadata, bulk quotes, OHLCV bars, public portfolios, post feeds, and post comments).
- **Default Headers**:
  ```http
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36
  Accept: application/json
  ```

---

## 📑 Endpoint Directory

| Category | Method | Endpoint | Auth | Description |
| :--- | :---: | :--- | :---: | :--- |
| **Leaderboards** | `GET` | `/stonks/security/leaderboard` | Public | Trending & Top-Owned Stock Leaderboards |
| **Tickers** | `GET` | `/stonks/security/ticker/{tickerSymbol}` | Public | Detailed ticker metadata, verified holders, and aggregate $ held |
| **Pricing** | `GET` | `/stonks/tickers/prices` | Public | Multi-ticker real-time price quotes |
| **Pricing** | `GET` | `/stonks/securities/prices` | Public | Multi-security-ID real-time price quotes |
| **Market Data** | `GET` | `/stonks/security/{securityId}/historic_prices` | Public | Full OHLCV historical candlestick bars (1D, 1m, etc.) |
| **Portfolios** | `GET` | `/stonks/public/portfolio/{profileId}/summary/live` | Public | Live verified portfolio positions, shares, cost basis, & P&L |
| **Profiles** | `GET` | `https://afterhour.com/{username}` | Public | Web scraper for `profile_id`, follower count, & bio |
| **Feeds** | `GET` | `/social/feed` | Public | Platform-wide or user-specific post & trade feed |
| **Posts** | `GET` | `/public/post/{hashedPostNumber}` | Public | Single post details with view counts, reactions, & comments |
| **Creators** | `GET` | `/profiles/leaderboard/suggested-follows` | Bearer | Creator tips / top suggested follows leaderboard |

---

## 1. Stock Leaderboard & Trending Securities

### `GET /stonks/security/leaderboard`
Fetches the ranked list of securities displayed on the mobile app's **Top Stocks** screen.

- **Query Parameters**:
  - `take` *(integer, optional)*: Number of items to return. Min `1`, Max `50`. Defaults to `15`.
  - `cursor` *(integer, optional)*: Offset pagination cursor (`0`, `50`, `100`, ...).
- **Total Universe**: **16,378** securities tracked.

#### Response Structure
```json
{
  "take": 50,
  "totalCount": 16378,
  "cursor": 50,
  "securities": [
    {
      "change": "new",
      "security": {
        "marketCap": 20704407009,
        "ownerCount": 321,
        "totalValue": 13500746.24,
        "url": "https://www.nvidia.com",
        "isoCurrencyCode": "USD",
        "employeeCount": 29600,
        "headquarters": "Santa Clara, CA",
        "price": {
          "symbol": "NVDA",
          "price": 233.95,
          "asOf": "2026-10-02T21:23:59.980Z",
          "version": 1,
          "session": {
            "open": 230.50,
            "high": 235.10,
            "low": 229.80,
            "close": 233.95,
            "volume": 48210390,
            "change": 3.10,
            "changePercent": 1.338,
            "earlyTradingChange": 0.50,
            "earlyTradingChangePercent": 0.22,
            "lateTradingChange": -0.15,
            "lateTradingChangePercent": -0.06
          }
        },
        "security": {
          "id": "sec_10c903210b8e49ac9fa23c57679407f0",
          "type": "EQUITY",
          "name": "NVIDIA Corporation",
          "friendlyName": "NVIDIA",
          "tickerSymbol": "NVDA",
          "rootTickerSymbol": "NVDA",
          "isCashEquivalent": false,
          "shortDescription": "NVIDIA Corporation designs graphics processing units...",
          "createdAt": "2023-02-05T22:08:02.606Z",
          "updatedAt": "2026-06-24T16:55:18.481Z",
          "iconUrl": "https://d21mnq29ucedqg.cloudfront.net/stonks/security/sec_10c903210b8e49ac9fa23c57679407f0/icon",
          "logoUrl": "https://d21mnq29ucedqg.cloudfront.net/stonks/security/sec_10c903210b8e49ac9fa23c57679407f0/logo",
          "chatroom": {
            "matrixId": "!ZS1E9scUSfKzDLrlsyku0w:chatapi.afterhour.chat",
            "memberCount": 23328,
            "onlineCount": 2,
            "type": "SECURITY",
            "name": null,
            "isActive": true
          }
        },
        "ownersSample": [
          {
            "id": "prf_c4a6425553bb4d2c964e029917d791b7",
            "username": "SlowmoInvestor",
            "memberNumber": 1846,
            "profilePhotoUrl": "https://d21mnq29ucedqg.cloudfront.net/profiles/...",
            "numFollowers": 1846,
            "hasConnectedItems": true
          }
        ]
      }
    }
  ]
}
```

> **Client Sorting Tip**:
> - **Trending Tab**: Native ordering returned by `/stonks/security/leaderboard`.
> - **Owners Tab**: Sort `securities` by `item.security.ownerCount` descending.
> - **Whale Value Tab**: Sort `securities` by `item.security.totalValue` descending.

---

## 2. Single Ticker Deep-Dive

### `GET /stonks/security/ticker/{tickerSymbol}`
Fetches aggregate community exposure and metadata for a specific ticker (e.g. `NVDA`, `TSLA`, `MSTR`).

- **Path Parameters**:
  - `tickerSymbol` *(string, required)*: Stock or crypto symbol.
- **Sample Request**:
  ```http
  GET /stonks/security/ticker/MSTR HTTP/1.1
  Host: api.afterhour.com
  User-Agent: Mozilla/5.0
  ```

#### Response Fields
- `ownerCount`: Exact number of verified AfterHour accounts holding the asset.
- `totalValue`: Total aggregate dollar value held across the platform.
- `price`: Live session pricing, volume, and pre/post-market performance.
- `security.chatroom`: Associated Matrix chatroom ID, total member count, and live online users.
- `ownersSample`: Array of notable verified accounts holding this position.

---

## 3. Real-Time Bulk Price Quotes

### `GET /stonks/tickers/prices`
Fetches real-time price snapshots for up to 50 tickers in a single HTTP call.

- **Query Parameters**:
  - `tickers` *(string, required)*: Comma-separated list of symbols (e.g. `NVDA,TSLA,SPY,AAPL`).
- **Response**:
  ```json
  {
    "prices": {
      "NVDA": {
        "price": 233.95,
        "asOf": "2026-10-02T21:23:59.980Z",
        "session": { "changePercent": 1.338, "volume": 48210390 }
      },
      "TSLA": {
        "price": 370.53,
        "asOf": "2026-10-02T21:23:58.120Z",
        "session": { "changePercent": 4.641, "volume": 61289100 }
      }
    }
  }
  ```

---

## 4. Market Data / Historic OHLCV Candlestick Bars

### `GET /stonks/security/{securityId}/historic_prices`
A zero-auth market data proxy returning institutional-grade OHLCV candlestick bars with Volume-Weighted Average Price (VWAP) and trade counts.

- **Path Parameters**:
  - `securityId` *(string, required)*: AfterHour internal security ID (e.g. `sec_10c903210b8e49ac9fa23c57679407f0`).
- **Query Parameters (Strict NestJS Validation)**:
  - `multiplier` *(integer, required)*: Bar width factor (`>= 1`). Usually `1`.
  - `timespan` *(string, required)*: Must be one of `second`, `minute`, `hour`, `day`, `week`, `month`, `quarter`, `year`.
  - `start` *(string, required)*: ISO 8601 UTC timestamp (e.g. `2026-08-01T00:00:00.000Z`).
  - `end` *(string, required)*: ISO 8601 UTC timestamp (e.g. `2026-10-02T00:00:00.000Z`).

#### Sample Response
```json
{
  "prices": [
    {
      "timestamp": "2026-09-01T04:00:00.000Z",
      "symbol": "NVDA",
      "open": 228.15,
      "high": 234.80,
      "low": 227.50,
      "close": 233.95,
      "volume": 48210390,
      "volumeWeightedAveragePrice": 231.8492,
      "numberOfTrades": 381920
    }
  ]
}
```

---

## 5. User Portfolio & Holdings Data

### `GET /stonks/public/portfolio/{profileId}/summary/live`
Returns the real-time verified brokerage holdings of any user who has connected their account and opted to make their positions public.

- **Path Parameters**:
  - `profileId` *(string, required)*: User's internal ID (`prf_*`).
- **Response Structure**:
  ```json
  {
    "ownerId": "prf_c4a6425553bb4d2c964e029917d791b7",
    "totalValue": 16147723.98,
    "cashBalance": 54210.00,
    "costBasis": 1285375.08,
    "profit": 13526546.37,
    "profitPercent": 975.28,
    "profitToday": 182390.45,
    "profitTodayPercent": 1.14,
    "verifiedAsOf": "2026-10-02T21:40:00.000Z",
    "lastSyncedAt": "2026-10-02T21:35:00.000Z",
    "positionSnapshots": [
      {
        "id": "pos_92837194",
        "tickerSymbol": "AAPL",
        "securityName": "Apple",
        "type": "EQUITY",
        "quantity": 28000.0,
        "value": 9343320.00,
        "costBasis": 598807.00,
        "profit": 8744513.00,
        "profitPercent": 1460.32,
        "price": 333.51
      },
      {
        "id": "pos_18293049",
        "tickerSymbol": "NVDA",
        "securityName": "Nvidia",
        "type": "EQUITY",
        "quantity": 20000.0,
        "value": 4679000.00,
        "costBasis": 76100.00,
        "profit": 4602900.00,
        "profitPercent": 6048.49,
        "price": 233.95
      }
    ]
  }
  ```

---

## 6. User Profile Resolution

### `GET https://afterhour.com/{username}`
AfterHour does not use usernames directly in API routes. Instead, query the web profile to extract the internal profile ID (`prf_*`) and embedded Next.js profile telemetry.

#### Python Profile Resolver
```python
import re
import json
import urllib.request

def get_profile(username: str) -> dict:
    url = f"https://afterhour.com/{username}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode("utf-8")
    
    # Locate Next.js hydration payload
    id_match = re.search(r'"id":"(prf_[a-f0-9]+)"', html)
    if not id_match:
        raise ValueError(f"Profile @{username} not found")
    
    profile_id = id_match.group(1)
    followers = re.search(r'"numFollowers":(\d+)', html)
    following = re.search(r'"numFollowing":(\d+)', html)
    likes = re.search(r'"numTotalLikes":(\d+)', html)
    bio = re.search(r'"bio":"(.*?)"', html)
    
    return {
        "username": username,
        "profile_id": profile_id,
        "followers": int(followers.group(1)) if followers else 0,
        "following": int(following.group(1)) if following else 0,
        "likes": int(likes.group(1)) if likes else 0,
        "bio": bio.group(1).encode().decode("unicode_escape") if bio else "",
    }
```

---

## 7. Social Feed & Post History

### `GET /social/feed`
Paginates through post, trade, and trade collection feeds.

- **Query Parameters**:
  - `contentTypes` *(string or array, required)*: Allowed values: `post`, `trade`, `trade_collection`.
  - `take` *(integer, optional)*: Page size (`1` to `100`, default `50`).
  - `cursor` *(integer or string, optional)*: Pagination cursor.
  - `authorId` *(string, optional)*: Filter by internal `prf_*` ID.
  - `tickerSymbol` *(string, optional)*: Filter feed by ticker (e.g. `NVDA`).
  - `primaryTopicKey` *(string, optional)*: Topic filter (`gain`, `loss`, `yolo`, `chart`, `dd`, `funny`, `crypto`).

---

## 8. Post Deep-Dive & Comments

### `GET /public/post/{hashedPostNumber}`
Retrieves a specific post by its short hash (from its share URL, e.g. `https://afterhour.com/{user}/{hash}/{slug}`).

- **Sample Request**:
  ```http
  GET /public/post/bw8L HTTP/1.1
  Host: api.afterhour.com
  User-Agent: Mozilla/5.0
  ```
- **Returns**:
  - `viewCount`: Total view count on mobile and web.
  - `reactionCounts`: Map of emoji reactions (`thumbsUp`, `rocket`, `fire`, etc.).
  - `comments`: Full list of comments, each containing comment text, timestamps, and author profile details.
  - `positionSnapshots`: Brokerage positions linked directly to this post.

---

## 9. Python SDK Wrapper Recipe

A self-contained client to interact with all discovered AfterHour endpoints:

```python
import json
import urllib.request
from typing import Any

class AfterHourClient:
    BASE_URL = "https://api.afterhour.com"
    UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

    def _get(self, path: str) -> Any:
        url = f"{self.BASE_URL}{path}" if path.startswith("/") else path
        req = urllib.request.Request(url, headers={"User-Agent": self.UA})
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def get_stock_leaderboard(self, take: int = 50, cursor: int = 0) -> dict:
        return self._get(f"/stonks/security/leaderboard?take={take}&cursor={cursor}")

    def get_ticker(self, symbol: str) -> dict:
        return self._get(f"/stonks/security/ticker/{symbol}")

    def get_prices(self, symbols: list[str]) -> dict:
        return self._get(f"/stonks/tickers/prices?tickers={','.join(symbols)}")

    def get_historic_bars(self, security_id: str, start_iso: str, end_iso: str, timespan: str = "day") -> list[dict]:
        endpoint = f"/stonks/security/{security_id}/historic_prices?multiplier=1&timespan={timespan}&start={start_iso}&end={end_iso}"
        data = self._get(endpoint)
        return data.get("prices", [])

    def get_public_portfolio(self, profile_id: str) -> dict:
        return self._get(f"/stonks/public/portfolio/{profile_id}/summary/live")

    def get_post_details(self, post_hash: str) -> dict:
        return self._get(f"/public/post/{post_hash}")
```
