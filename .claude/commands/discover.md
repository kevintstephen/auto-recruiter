---
description: Find interesting/funded AI & robotics companies and add/update them in the Companies database
---

Read `CLAUDE.md` first for the operating rules, scoring rubric, and hard rules — apply them throughout this command.

1. Load `config/targets.yaml` and `config/shortlist.yaml`.
2. **Shortlist companies:** for every company in `shortlist.yaml`, search for recent news (funding, launches, notable posts) regardless of whether a trigger fires — they're screened every run.
3. **Funding trigger:** web search for AI/robotics companies that raised ≥$50M in the last 90 days (TechCrunch, Axios Pro Rata, and similar sources). Only companies matching `company_types` and `stage` in `targets.yaml`.
4. For every candidate company, judge each rubric dimension yourself (funding momentum, investor tier, AI-native status, geo — see `CLAUDE.md`), then run `python3 scripts/scoring.py --funding-momentum X --investor-tier X --ai-native X --geo X` to get the total and check it against the thresholds in `config/targets.yaml` — don't add the numbers by hand.
5. **Dedup before writing:** search the Companies database for an existing row matching the company name.
   - If it exists: update `AI/Robotics Category`, `Stage`, `Last Round`, `HQ Location` if changed, and append new findings to `Notes` (don't overwrite anything Kevin wrote manually).
   - If it doesn't exist: create a new row with `Discovery Source` set to `Shortlist` or `Funding Trigger` as appropriate.
6. Skip companies scoring below `scoring.min_score_to_map_contacts` in `targets.yaml` unless they're on the shortlist (shortlist companies always get a row, regardless of score, so Kevin can see why they didn't clear the bar).
7. Append a "Discover" section to `runs/YYYY-MM-DD.md` (create the file if it doesn't exist) listing: companies screened, scores, and which ones are new vs. updated.
8. If `config/shortlist.yaml` or `config/targets.yaml` is missing or a data source fails, degrade gracefully and note it in the run log rather than failing.
