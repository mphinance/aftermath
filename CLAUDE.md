# AfterMath

Forensic scraper + analytics over AfterHour trader post histories. Plain Python scripts, no server.

## Adding a trader

1. `python3 download_single_trader_lifetime.py <username>` → `data/following/@<u>_all_posts.json` + `reports/posts/@<u>_lifetime.md`
2. `python3 followthrough.py --json reports/analysis/followthrough.json` (recomputes all traders; diff should only add the new row)
3. Dossier → `reports/dossiers/@<u>_quant_profile.md` (prompt in `FORENSIC_AUTOPSY_PIPELINE.md`), copied to `reports/dossiers/sonnet/`
4. `python3 parse_dossiers.py --out reports/analysis/verdicts_flash.json` and `--dir reports/dossiers/sonnet --out reports/analysis/verdicts_sonnet.json`

## Position history (broker-verified)

Posts carry a `portfolioSnapshot` with every leg (strike, expiry, qty, basis, P&L); `normalize()` drops it, so use:

- `python3 positions.py <u>` → `data/positions/@<u>_positions.json` (account series, legs, diffed changes) + `reports/positions/@<u>_position_changes.md`
- `python3 fetch_prices.py <u>` (needs yfinance, not in requirements) → `data/prices/@<u>_prices.json` daily bars + earnings dates

A snapshot only holds legs for the tickers tagged on that post — absence elsewhere means nothing. Option `quantity` is shares (×100 contracts); shorts negative. $SQ history lives under XYZ.

## Gotchas

- `amount_k` is account value in **thousands** of dollars (`afterhour.py` divides by 1000). 57382 = $57.4M, not $57.4k.
- Paths in `FORENSIC_AUTOPSY_PIPELINE.md` point at the old `/home/mpha/artemis/afterhour/` location; use this repo.
- `parse_dossiers.py` defaults `--out` to `./verdicts.json` in cwd; don't leave that file in the repo.
- Dossier metadata block format must match existing dossiers or `parse_dossiers.py` misses fields.
- `followthrough.py` credits a close to every ticker in a post containing any exit word, so omnibus posts inflate follow-through.
