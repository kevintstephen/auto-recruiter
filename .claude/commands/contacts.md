---
description: Find contacts with shared background at qualifying companies and add/update them in the Contacts database
---

Read `CLAUDE.md` first for the operating rules, contact priority tiers, and hard rules — apply them throughout this command.

1. Query the Companies database for rows scoring ≥ `scoring.min_score_to_map_contacts` (see `config/targets.yaml`), or on the shortlist, that don't yet have a mapped contact with `Outreach Status` other than blank/stale.
2. **1st-degree:** if `data/connections.csv` exists, match its rows against each qualifying company by company name. Any match is a `Bridge = 1st-degree` contact — always worth adding.
3. **CEO:** for each qualifying company without a 1st-degree match, do one targeted web search/fetch of the company's public "About"/"Team" page or recent press to find the CEO's name and title.
4. **Alumni match:** targeted web search of the company's leadership/team page for mentions of Harvard, Stanford GSB, Knight-Hennessy, Bain & Company, or Cambio AI. This is a single-person lookup per company — never bulk LinkedIn scraping. If nothing turns up, leave it — don't guess.
5. **Dedup before writing:** search the Contacts database for an existing row matching person name + company. Update rather than duplicate; append new findings to `Notes` instead of overwriting anything Kevin edited manually.
6. **Email lookup:** for each contact found, run `python3 scripts/apollo.py match-person --first-name ... --last-name ... --org "..."` (add `--linkedin-url` if you have one — it improves match accuracy). If the company's domain is ambiguous, run `python3 scripts/apollo.py enrich-org --name "..."` first to resolve it. If Apollo returns no match or an error (e.g. no API access on the current plan), leave `Email` blank and note it in the run log — don't fabricate an address.
7. For each new/updated contact, set `Bridge`, `Bridge Detail` (the specific connection, e.g. "Harvard '19, overlapped with Kevin at Bain 2020-21"), `Source`, `Title`, `Email`, and relate it to the Company row. Leave `Outreach Status` as `Not Contacted` for new rows.
8. Append a "Contacts" section to `runs/YYYY-MM-DD.md` listing: companies checked, contacts found (with bridge type), and any qualifying company where no contact could be found.
9. If `data/connections.csv` is missing, degrade gracefully — skip the 1st-degree step, note it in the run log, and continue with CEO/alumni lookups.

