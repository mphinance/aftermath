#!/usr/bin/env python3
"""
Pull the TraderMatrix verdict blocks out of the Artemis forensic dossiers into JSON.

The dossiers are written by independent subagent runs off one shared prompt, so the
prose is consistent but the *formatting* of section 5 drifted three ways: markdown
tables, bold bullets, and h4 headings. Each field below is tried against all three.

    python3 tools/parse_dossiers.py                      # -> verdicts.json + coverage
    python3 tools/parse_dossiers.py --cards              # post-ready markdown blocks
    python3 tools/parse_dossiers.py --only mphinance
"""
import argparse
import json
import os
import re
import sys
from glob import glob
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DOSSIER_DIR = str(BASE_DIR / "reports" / "dossiers")
OUT_JSON = "verdicts.json"


def _clean(value):
    if value is None:
        return None
    value = value.strip().strip("`*").strip()
    value = re.sub(r"\s+", " ", value)
    return value or None


def _cells(line):
    """Split a markdown table row into cleaned cells, stripping emphasis and approx signs."""
    if "|" not in line:
        return []
    parts = [c.strip() for c in line.strip().strip("|").split("|")]
    return [re.sub(r"[*`~≈]|\s+", lambda m: "" if m.group(0) != " " else " ", c).strip() for c in parts]


def _table_rows(text):
    for line in text.splitlines():
        cells = _cells(line)
        if len(cells) >= 2 and not re.fullmatch(r"[-: ]*", cells[0]):
            yield cells


def _score_in(cell):
    match = re.search(r"(\d{1,3})\s*/\s*100", cell)
    return int(match.group(1)) if match else None


def _first(text, patterns, group=1, flags=re.I | re.M):
    for pattern in patterns:
        match = re.search(pattern, text, flags)
        if match:
            return _clean(match.group(group))
    return None


def classification(text, rank):
    """rank is 'Primary', 'Secondary' or 'Tertiary'."""
    label = rf"{rank}(?: (?:System Tag|Thematic Tag|Classification))?"
    return _first(text, [
        rf"^\|\s*\**{label}\**\s*\|\s*`?([^|`]+?)`?\s*\|",   # | Primary Classification | X |
        rf"\*\*{label}\s*:\s*`([A-Z0-9_]+)`\s*\*\*",           # - **Primary: `X`** — desc
        rf"\*\*{label}\s*:?\*\*\s*:?\s*`?([A-Z0-9_ /&]+)`?",  # **Primary:** `X`  /  **Primary Tag**: `X`
        rf"^#{{2,5}}\s*\d*\.?\s*{label}\s*:\s*`?([^`\n]+)`?",  # #### 1. PRIMARY CLASSIFICATION: `X`
    ])


def alpha_score(text):
    """Returns (score_out_of_100, note, basis). Scales and spellings both drifted."""
    hundred = [
        r"COMPOSITE ALGORITHMIC ALPHA SCORE\s*\|\s*(\d{1,3})\s*/\s*100\s*\|\s*([^|]*)",
        r"^\|\s*(?:Composite )?(?:Algorithmic )?(?:Alpha Score|Quantitative Expectancy Score|"
        r"Execution Alpha Expectancy|Algorithmic Alpha Score)\s*\|\s*(\d{1,3})\s*/\s*100\s*([^|]*)",
        r"Algorithmic Alpha Score of \*{0,2}(\d{1,3})\s*/\s*100\*{0,2}()",
        r"\*\*Algorithmic Alpha Score\*\*\s*:?\s*\*{0,2}(\d{1,3})\s*/\s*100\*{0,2}()",
        # **ALPHA SCORE: 14 / 100** — colon and number inside the emphasis
        r"\*{0,2}(?:Composite |Algorithmic )?ALPHA SCORE\s*:\s*\*{0,2}(\d{1,3})\s*/\s*100()",
    ]
    for pattern in hundred:
        match = re.search(pattern, text, re.I | re.M)
        if match:
            note = _clean(match.group(2)) if match.lastindex and match.lastindex >= 2 else None
            return int(match.group(1)), (note.strip("()").strip() if note else None), "stated"

    # Table row whose label says "composite" or "alpha score", score in any later cell.
    for cells in _table_rows(text):
        if "composite" in cells[0].lower() or "alpha score" in cells[0].lower():
            for cell in cells[1:]:
                score = _score_in(cell)
                if score is not None:
                    return score, _clean(cells[0]), "stated"

    # Some runs scored out of 10 instead of 100.
    match = re.search(r"AGGREGATE COMPOSITE SCORE\s*\|\s*([\d.]+)\s*\|\s*([^|]*)", text, re.I)
    if match:
        note = _clean(match.group(2))
        return round(float(match.group(1)) * 10), note, "rescaled_from_10"

    # No composite anywhere: average the category rows rather than invent one.
    rows = subscores(text)
    if len(rows) >= 3:
        mean = round(sum(r["score"] for r in rows) / len(rows))
        return mean, f"derived from {len(rows)} category scores, no composite stated", "derived"

    return None, None, None


def subscores(text):
    """Category rows scored out of 100, from both the ASCII scorecard and md tables."""
    rows = []
    seen = set()
    for cells in _table_rows(text):
        score = _score_in(cells[1]) if len(cells) > 1 else None
        if score is None:
            continue
        name = re.sub(r"^\d+\.\s*", "", cells[0]).strip()
        if not name or len(name) < 4:
            continue
        lowered = name.lower()
        if any(
            token in lowered
            for token in ("composite", "alpha score", "quantitative expectancy score", "execution alpha expectancy")
        ):
            continue
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        rows.append({"category": name, "score": score})
    return rows


def expectancy(text):
    win = _first(text, [r"Win Rate[^:|\n]{0,40}[:|]\s*\*{0,2}([\d.]+)\s*%"])
    payoff = None
    match = re.search(r"Payoff Ratio[^:|\n]{0,40}[:|]\s*\*{0,2}([\d.]+)\s*:\s*([\d.]+)", text, re.I)
    if match:
        payoff = f"{match.group(1)} : {match.group(2)}"
    ev = _first(text, [r"Expected Value[^:|\n]{0,45}[:|]\s*\*{0,2}([+\-]?[\d.]+)\s*R"])

    # Some runs decline to state a number and give a qualitative read instead.
    # That is a finding, not a gap, so keep the words.
    qualitative = []
    for cells in _table_rows(text):
        if "expectancy" in cells[0].lower() and len(cells) > 1 and not _score_in(cells[1]):
            value = _clean(cells[1])
            if value and len(value) < 120:
                qualitative.append({"scope": _clean(cells[0]), "read": value})

    for match in re.finditer(r"\*\*Expectancy([^*]{0,60})\*\*\s*:?\s*(.+)", text):
        read = _clean(re.sub(r"[*`]", "", match.group(2)))
        if read and len(read) > 20:
            qualitative.append({"scope": "Expectancy" + (match.group(1) or "").strip(" :"), "read": read[:300]})

    if not any([win, payoff, ev]) and not qualitative:
        return None
    return {
        "win_rate_pct": float(win) if win else None,
        "payoff_ratio": payoff,
        "expected_value_r": ev,
        "qualitative": qualitative or None,
    }


def archetype(text):
    return _first(text, [
        r"^#{2,4}\s*\d+\.\d+\s*(?:The Archetype|Trader Philosophy & Archetype)\s*:\s*(.+)$",
        r"^#{2,4}[^\n]*Archetype\s*:\s*(.+)$",
    ])


DIRECTIVE_KINDS = [
    ("ingest", r"Ingestion Directives?"),
    ("fade", r"Contrarian Fade Directives?"),
    ("firewall", r"(?:Risk )?(?:Blacklists?|Firewalls?)"),
    ("exit", r"Exit Rules?"),
]


def directives(text):
    """Bolded bullet headers under each of the four Artemis directive blocks."""
    out = {}
    for key, heading in DIRECTIVE_KINDS:
        # Either an h2-h5 heading, or a bolded run-in label on its own line.
        match = re.search(
            rf"^(?:#{{2,5}}[^\n]*{heading}[^\n]*|\*\*[^*\n]*{heading}[^*\n]*\*\*:?)\s*$",
            text, re.I | re.M,
        )
        if not match:
            continue
        body = text[match.end():]
        stop = re.search(r"^(?:#{2,5}\s|\*\*[A-Z][^*\n]{6,}\*\*:?\s*$)", body, re.M)
        if stop:
            body = body[: stop.start()]

        items = []
        for line in re.findall(r"^\s*(?:[-*]|\d+\.)\s+(.+)$", body, re.M):
            item = re.sub(r"[*`]", "", line).strip()
            # Keep the instruction, drop the trailing justification.
            item = re.split(r"\s+[—–]\s+|(?<=[a-z])\.\s+(?=[A-Z])", item)[0].strip()
            item = item.rstrip(" .:,;")
            if 12 < len(item) <= 180:
                items.append(item)
        if items:
            out[key] = items
    return out


def posting(text):
    posts = _first(text, [r"([\d,]+)\s+lifetime posts", r"^\|\s*Total (?:Lifetime )?Posts\s*\|\s*([\d,]+)"])
    cadence = _first(text, [r"([\d.]+)\s*posts?\s*/\s*week", r"\((\d+)\s*Posts?/Week\)", r"Why\s+\d+\s+Posts a Week"])
    return {
        "lifetime_posts": int(posts.replace(",", "")) if posts else None,
        "posts_per_week": float(cadence) if cadence and re.fullmatch(r"[\d.]+", cadence) else cadence,
    }


def parse(path):
    text = open(path, encoding="utf-8").read()
    handle = os.path.basename(path).split("_quant_profile")[0].lstrip("@")

    verdict_match = re.search(r"^#{1,3}\s*5\.\s*Quantitative Verdict.*$", text, re.I | re.M)
    verdict = text[verdict_match.start():] if verdict_match else text
    score, note, basis = alpha_score(verdict)
    if score is None:
        score, note, basis = alpha_score(text)

    record = {
        "handle": handle,
        "source_file": os.path.basename(path),
        "archetype": archetype(text),
        "primary_classification": classification(verdict, "Primary") or classification(text, "Primary"),
        "secondary_classification": classification(verdict, "Secondary") or classification(text, "Secondary"),
        "tertiary_classification": classification(verdict, "Tertiary"),
        "alpha_score": score,
        "alpha_score_note": note,
        "alpha_score_basis": basis,
        "subscores": subscores(verdict),
        "expectancy": expectancy(verdict) or expectancy(text),
        "directives": directives(text),
        "posting": posting(text),
        "has_verdict_section": bool(verdict_match),
        "lines": text.count("\n") + 1,
    }
    record["missing"] = [
        field
        for field in ("archetype", "primary_classification", "secondary_classification", "alpha_score", "expectancy")
        if not record.get(field)
    ]
    return record


def card(rec):
    """Post-ready verdict block."""
    lines = [f"**@{rec['handle']}**"]
    if rec["archetype"]:
        lines.append(f"*{rec['archetype']}*")
    if rec["primary_classification"]:
        tags = rec["primary_classification"]
        if rec["secondary_classification"]:
            tags += f" / {rec['secondary_classification']}"
        lines.append(f"`{tags}`")
    if rec["alpha_score"] is not None:
        note = f" ({rec['alpha_score_note']})" if rec["alpha_score_note"] else ""
        lines.append(f"Alpha Score: **{rec['alpha_score']} / 100**{note}")
    for sub in rec["subscores"][:5]:
        lines.append(f"  {sub['category']}: {sub['score']} / 100")
    exp = rec["expectancy"]
    if exp:
        bits = []
        if exp.get("payoff_ratio"):
            bits.append(f"Payoff {exp['payoff_ratio']}")
        if exp.get("win_rate_pct") is not None:
            bits.append(f"Win rate {exp['win_rate_pct']}%")
        if exp.get("expected_value_r"):
            bits.append(f"EV {exp['expected_value_r']} R")
        if bits:
            lines.append("Expectancy: " + " · ".join(bits))
    for key, label in (("ingest", "Ingest"), ("fade", "Fade"), ("firewall", "Firewall"), ("exit", "Exit")):
        items = rec["directives"].get(key)
        if items:
            lines.append(f"{label}: " + "; ".join(items[:3]))
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=DOSSIER_DIR)
    ap.add_argument("--out", default=OUT_JSON)
    ap.add_argument("--only", help="substring match on handle")
    ap.add_argument("--cards", action="store_true", help="print post-ready markdown blocks")
    args = ap.parse_args()

    paths = sorted(glob(os.path.join(args.dir, "*_quant_profile.md")))
    if args.only:
        paths = [p for p in paths if args.only.lower() in os.path.basename(p).lower()]
    if not paths:
        sys.exit(f"no dossiers found in {args.dir}")

    records = [parse(p) for p in paths]
    # Don't write when only rendering cards or a filtered subset: it would clobber
    # a full parse with a partial one.
    if not args.cards and not args.only:
        with open(args.out, "w", encoding="utf-8") as fh:
            json.dump(records, fh, indent=2, ensure_ascii=False)

    if args.cards:
        for rec in records:
            print(card(rec))
            print()
        return

    print(f"parsed {len(records)} dossiers -> {args.out}\n")
    width = max(len(r["handle"]) for r in records) + 2
    for rec in records:
        score = f"{rec['alpha_score']:>3}/100" if rec["alpha_score"] is not None else "   ??? "
        gaps = ("MISSING: " + ", ".join(rec["missing"])) if rec["missing"] else "complete"
        print(f"  @{rec['handle']:<{width}} {score}  {(rec['primary_classification'] or '-')[:38]:<38} {gaps}")
    total = len(records)
    for field in ("archetype", "primary_classification", "alpha_score", "expectancy", "subscores", "directives"):
        got = sum(1 for r in records if r.get(field))
        print(f"\n  {field:<24} {got}/{total}", end="")
    print()


if __name__ == "__main__":
    main()
