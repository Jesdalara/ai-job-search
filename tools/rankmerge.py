#!/usr/bin/env python3
"""Merge /rank scoring-agent output into job_scraper/seen_jobs.json, safely.

Why this exists
---------------
`/rank` Step 4 has always specified that `strengths` and `gaps` are persisted
verbatim. Across roughly 200 scored postings in Aug 2026 **only the scores and
flags survived** - the bullets were reported to the user and dropped, because
the write-back was a hand-written script each time rather than part of the
command. Re-deriving them costs a fetch and an agent per posting.

The second reason is safety. Two failure modes in this pipeline corrupt data
silently and permanently, and prose in a command file did not stop either:

  * A throttled fetch is indistinguishable from a dead posting. On 28 Aug 2026,
    30 rapid sequential calls returned "no data" for all 30, including a posting
    verified live minutes earlier. Writing that batch would have marked live
    roles `expired` forever, and nothing re-checks an expired row.
  * Scores from different rubric generations are not comparable (measured drift
    +6/+8/+9 on byte-identical descriptions), and an entry with no `rubric`
    stamp cannot be told apart from a current one.

So this tool refuses an all-failed batch, refuses to downgrade a real score,
and refuses to write a score without a rubric. Those are hard stops, not
warnings.

Usage
-----
    python tools/rankmerge.py results.json --rubric lane-table-v2
    python tools/rankmerge.py results.json --rubric lane-table-v2 --dry-run
    python tools/rankmerge.py results.json --rubric lane-table-v2 \
        --scope-note "only local + remote roles; 285 international skipped"

`results.json` is the concatenated Step 2 agent output: a JSON array of scoring
objects, or an object with a "results" array.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import shutil
import sys
from pathlib import Path

WEIGHTS = {"technical": 0.30, "experience": 0.25, "behavioral": 0.15, "career": 0.30}
BANDS = [(75, "Strong Fit"), (60, "Good Fit"), (45, "Moderate Fit"), (30, "Weak Fit"), (0, "Poor Fit")]

CARRY = ["location", "language_gate", "language_note", "deadline", "strengths", "gaps",
         "language", "visa", "visa_note", "portfolio_required", "still_open", "band"]


def verdict_for(score: float) -> str:
    for floor, name in BANDS:
        if score >= floor:
            return name
    return "Poor Fit"


def overall(scores: dict) -> float:
    missing = [k for k in WEIGHTS if k not in scores]
    if missing:
        raise ValueError(f"missing score dimensions: {', '.join(missing)}")
    return round(sum(scores[k] * w for k, w in WEIGHTS.items()), 1)


def load_results(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("results", data.get("jobs", []))
    if not isinstance(data, list):
        raise SystemExit("FAIL  results file must be a JSON array (or {\"results\": [...]})")
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", type=Path)
    ap.add_argument("--rubric", required=True,
                    help="framework_version from 04-job-evaluation.md frontmatter")
    ap.add_argument("--seen", type=Path, default=Path("job_scraper/seen_jobs.json"))
    ap.add_argument("--scope-note", help="what this run deliberately did not rank, and why")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force-expired", action="store_true",
                    help="override the all-failed-batch guard. Only after a spaced retry confirmed it.")
    args = ap.parse_args()

    results = load_results(args.results)
    if not results:
        print("FAIL  results file is empty")
        return 2

    store = json.loads(args.seen.read_text(encoding="utf-8"))
    seen = store["seen"] if "seen" in store else store

    scored = [r for r in results if r.get("status") == "scored"]
    expired = [r for r in results if r.get("status") == "expired"]
    unknown = [r for r in results if r.get("status") == "unknown"]
    other = [r for r in results if r.get("status") not in ("scored", "expired", "unknown")]

    print(f"\n  batch       {len(results)} results: {len(scored)} scored, "
          f"{len(expired)} expired, {len(unknown)} unknown"
          + (f", {len(other)} MALFORMED" if other else ""))

    # --- Guard 1: an all-failures batch is a throttling signal, not a finding.
    failed = len(expired) + len(unknown)
    if failed == len(results) and len(results) >= 5 and not args.force_expired:
        print(f"\n  FAIL  every one of {len(results)} fetches failed.")
        print("        That is the signature of throttling, not of {0} dead postings."
              .format(len(results)))
        print("        Measured 28 Aug 2026: 30/30 failed while a posting verified live minutes")
        print("        earlier was among them. Writing this batch would mark live roles expired,")
        print("        permanently, and nothing re-checks an expired row.")
        print("        Back off, retry the slice spaced out, and re-run. Use --force-expired only")
        print("        after a second spaced attempt confirmed the postings really are gone.\n")
        return 3

    if other:
        for r in other:
            print(f"  FAIL  {r.get('key','<no key>')}: unusable status {r.get('status')!r}")
        return 2

    now = dt.date.today().isoformat()
    updates, skipped, missing_keys, errors = 0, [], [], []

    for r in results:
        key = r.get("key")
        if key not in seen:
            missing_keys.append(key)
            continue
        entry = seen[key]
        status = r["status"]

        if status == "unknown":
            # Guard 2: never destroy a real score with a failed retrieval.
            if entry.get("status") == "ranked":
                skipped.append((key, "unknown fetch, existing score kept"))
                continue
            entry["status"] = "unknown"
            entry["last_fetch_failed"] = now
            updates += 1
            continue

        if status == "expired":
            entry["status"] = "expired"
            entry["expired_confirmed"] = now
            updates += 1
            continue

        try:
            score = overall(r["scores"])
        except (KeyError, ValueError) as exc:
            errors.append(f"{key}: {exc}")
            continue

        entry["status"] = "ranked"
        entry["rank_score"] = score
        entry["rank_verdict"] = verdict_for(score)
        entry["rank_date"] = now
        entry["rubric"] = args.rubric          # Guard 3: never a score without a rubric.
        for field in CARRY:
            if field in r:
                entry[field] = r[field]
        if args.scope_note:
            entry.pop("rank_scope_note", None)  # this one WAS ranked
        updates += 1

    if args.scope_note:
        for key, entry in seen.items():
            if entry.get("status") == "new":
                entry["rank_scope_note"] = f"{now}: {args.scope_note}"

    if errors:
        for e in errors:
            print(f"  FAIL  {e}")
        return 2
    if missing_keys:
        print(f"  warn  {len(missing_keys)} key(s) not in {args.seen.name}: "
              + ", ".join(str(k)[:60] for k in missing_keys[:3])
              + (" ..." if len(missing_keys) > 3 else ""))

    for key, why in skipped:
        print(f"  warn  kept existing score for {key[:70]} ({why})")

    if args.dry_run:
        print(f"\n  dry-run     would update {updates} entries with rubric {args.rubric}\n")
        return 0

    backup = args.seen.with_suffix(f".{now}.bak.json")
    if not backup.exists():
        shutil.copy2(args.seen, backup)
    args.seen.write_text(json.dumps(store, indent=1, ensure_ascii=False), encoding="utf-8")

    ranked_total = sum(1 for e in seen.values() if e.get("status") == "ranked")
    current = sum(1 for e in seen.values() if e.get("rubric") == args.rubric)
    print(f"\n  written     {updates} entries updated, rubric {args.rubric}")
    print(f"  backup      {backup.name}")
    print(f"  store       {ranked_total} ranked total, {current} on the current rubric"
          + (f", {ranked_total - current} STALE and not comparable" if ranked_total > current else ""))
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
