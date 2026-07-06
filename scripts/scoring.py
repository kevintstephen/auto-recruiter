#!/usr/bin/env python3
"""Deterministic fit-score calculator for the Company scoring rubric in CLAUDE.md.

Claude still decides the *inputs* (is this company AI-native? which investor
tier? how recent/large is the round?) via research and judgment. This script
just adds them up correctly and checks them against the thresholds in
config/targets.yaml, so the arithmetic isn't being redone by hand each run.

Usage:
    python3 scripts/scoring.py --funding-momentum 20 --investor-tier 20 \
        --ai-native 25 --geo 10

Point ranges (see CLAUDE.md "Company fit scoring rubric"):
    --funding-momentum   0-35
    --investor-tier      0-20
    --ai-native          0-25
    --geo                0-20
"""
import argparse
import os
import re
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_POINTS = {
    "funding_momentum": 35,
    "investor_tier": 20,
    "ai_native": 25,
    "geo": 20,
}
DEFAULT_MIN_SCORE_TO_MAP_CONTACTS = 50
DEFAULT_MIN_SCORE_FOR_COLD_OUTREACH = 80


def load_thresholds():
    """Read the two threshold ints out of config/targets.yaml without a YAML dependency.
    Falls back to defaults if the file is missing or the keys aren't found."""
    path = os.path.join(REPO_ROOT, "config", "targets.yaml")
    map_score = DEFAULT_MIN_SCORE_TO_MAP_CONTACTS
    cold_score = DEFAULT_MIN_SCORE_FOR_COLD_OUTREACH
    if os.path.exists(path):
        text = open(path).read()
        m = re.search(r"min_score_to_map_contacts:\s*(\d+)", text)
        if m:
            map_score = int(m.group(1))
        m = re.search(r"min_score_for_cold_outreach:\s*(\d+)", text)
        if m:
            cold_score = int(m.group(1))
    return map_score, cold_score


def main():
    parser = argparse.ArgumentParser(description="Score a company against the CLAUDE.md rubric")
    parser.add_argument("--funding-momentum", type=float, required=True)
    parser.add_argument("--investor-tier", type=float, required=True)
    parser.add_argument("--ai-native", type=float, required=True)
    parser.add_argument("--geo", type=float, required=True)
    args = parser.parse_args()

    values = {
        "funding_momentum": args.funding_momentum,
        "investor_tier": args.investor_tier,
        "ai_native": args.ai_native,
        "geo": args.geo,
    }
    for key, val in values.items():
        if not (0 <= val <= MAX_POINTS[key]):
            sys.exit(f"{key} must be between 0 and {MAX_POINTS[key]}, got {val}")

    total = sum(values.values())
    map_threshold, cold_threshold = load_thresholds()

    print(f"Fit Score: {total:g}/100")
    print(f"Clears contact-mapping threshold (>= {map_threshold}): {total >= map_threshold}")
    print(f"Clears cold-outreach threshold (>= {cold_threshold}): {total >= cold_threshold}")


if __name__ == "__main__":
    main()
